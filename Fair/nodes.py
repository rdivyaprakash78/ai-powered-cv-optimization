import os
from dotenv import load_dotenv
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser, RetryWithErrorOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from Fair.prompts import prompts
from langchain_groq import ChatGroq
from langchain_core.exceptions import OutputParserException
from typing import List, Literal
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
import time

load_dotenv()

os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"]="cv-improver"

class nodes :

    def __init__(self):
        self.llm = ChatOpenAI(model = "gpt-4o")
        self.api_key = os.getenv("GROQ_API_KEY")

    def template(self, pydantic_obj, prompt_tuple, prompt_value_dict):

        prompt = ChatPromptTemplate.from_messages(prompt_tuple)
        parser = PydanticOutputParser(pydantic_object=pydantic_obj)
        format_instructions =  parser.get_format_instructions()
        prompt_value_dict["format_instructions"] = str(format_instructions)
        chain = prompt | self.llm
        response = chain.invoke(prompt_value_dict)

        try :
            result = parser.parse(response.content)
        except OutputParserException as e:
            retry_parser = RetryWithErrorOutputParser.from_llm(parser=parser, llm=self.llm)
            prompt_value = prompt.format_prompt(**prompt_value_dict)
            result = retry_parser.parse_with_prompt(response.content, prompt_value)
            
        return result       
    
    def skills_analyzer(self, state):
        class skillsMissingObject (BaseModel):
            skill : str = Field(description = "Skill that is required for the job and is missing in the candidates CV")
            description : str = Field(description = "Description on why do you feel the skill is missing in the CV.")
            priority : int = Field(priority = "How important the skill is for the job")
            skill_type : Literal["technical", "non technical"] = Field(description = "Whether the skill is technical or non technical")

        class skillsPresentObject (BaseModel):
            skill : str = Field(description = "Skill that is required by the job and the candidate posses it")
            description : str = Field(description = "Description on why do you feel the candidate possesses the skill")
            priority : int = Field(priority = "How important the skill is for the job")
            skill_type : Literal["technical", "non technical"] = Field(description= "Whether the skill is technical or non technical")
            confidence : int = Field(confidence = "A confidence on how well the candidate posses that skill")

        class SkillsAnalyzerResponse(BaseModel):
            skills_missing : List[skillsMissingObject] = Field(description = "List of skills missing object.")
            skills_present : List[skillsPresentObject] = Field(description = "List of skills present object")

        prompt_tuple = [
            ("system", prompts["skills analyzer system prompt"]),
            ("human", prompts["skills analyzer human prompt"])
        ]

        prompt_value_dict = {
            "cv": state["cv"],
            "job_description": state["job_description"]
        }

        result = self.template(
            pydantic_obj= SkillsAnalyzerResponse,
            prompt_tuple = prompt_tuple,
            prompt_value_dict = prompt_value_dict
        )

        result.skills_present.sort(key=lambda obj: obj.confidence)
        result.skills_missing.sort(key=lambda obj: obj.priority, reverse=True)

        return {
            "skills_missing": result.skills_missing,
            "skills_present": result.skills_present
        }

    def question_generator(self, state):

        class question(BaseModel):
            question : str = Field(description = "Question to ask the candidate")

        prompt_tuple = [
            ("system", prompts["question generater prompt"])
        ]

        prompt_value_dict = {
            "skill" : state["skills_missing"][0].skill,
            "description" : state["skills_missing"][0].description
        }  

        result = self.template(
            pydantic_obj= question,
            prompt_tuple = prompt_tuple,
            prompt_value_dict = prompt_value_dict
        )                                                     

        return {question :result.question}