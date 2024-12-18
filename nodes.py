import os
from dotenv import load_dotenv
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from prompts import prompts
from langchain_groq import ChatGroq
from langchain_core.exceptions import OutputParserException
from typing import List, Literal
from pydantic import BaseModel, Field
import time

load_dotenv()

os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"]="cv-improver"

class nodes :

    def __init__(self):
        self.llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.25)
        self.api_key = os.getenv("GROQ_API_KEY")

    def template(self, pydantic_obj, prompt, prompt_value_dict):

        parser = PydanticOutputParser(pydantic_object=pydantic_obj)
        format_instructions =  parser.get_format_instructions()
        prompt_value_dict["format_instructions"] = str(format_instructions)
        chain = prompt | self.llm
        response = chain.invoke(prompt_value_dict)

        try :
            parser.parse(response.content)
            result = parser.parse(response.content)
        except OutputParserException as e:
            new_parser = OutputFixingParser.from_llm(parser=parser, llm=self.llm)
            result = new_parser.parse(response.content)

        return result
    
    def skills_needed(self,state):

        class skillsNeededObject (BaseModel):
            skill : str = Field(description = "Skill that is required for the job")
            description : str = Field(description = "Description of the skill")
            priority : str = Field(description = "Priority of the skill for the provided job description. Score out of 100.")
            skill_type : Literal["technical", "non technical"] = Field(description = "Whether the skill is technical or non technical")

        class skillsNeededResponse (BaseModel):
            skills_needed : List[skillsNeededObject] = Field(description = "List of skills_needed object. Each object have skill name, priority and their type.")

        prompt = ChatPromptTemplate.from_messages([
            ("system", prompts["skills needed system prompt"]),
            ("human", prompts["skills needed human prompt"])
        ]
        )
        
        prompt_value_dict = {
            "job_description": state["job_description"]
        }
 
        result = self.template(
            pydantic_obj= skillsNeededResponse,
            prompt = prompt,
            prompt_value_dict = prompt_value_dict
        )

        return {
            "skills_needed": result.skills_needed
        }
           
    
    def skills_missing(self, state):
        time.sleep(60)
        class skills_missing_object (BaseModel):
            skill : str = Field(description = "Skill that is required for the job and is present in the candidates CV")
            description : str = Field(description = "Description on why do you feel the skill is missing in the CV.")
            priority : str = Field(description = "Priority of the skill for the provided job description. Score out of 100.")
            skill_type : Literal["technical", "non technical"] = Field(description = "Whether the skill is technical or non technical")

        class SkillsMissingResponse(BaseModel):
            skills_missing : List[skills_missing_object] = Field(description = "List of skills_missing object. Each object have skill name, description and their priority.")

        prompt_tuple = [
            ("system", prompts["skills missing system prompt"]),
            ("human", prompts["skills missing human prompt"])
        ]
        prompt = ChatPromptTemplate.from_messages(prompt_tuple)

        prompt_value_dict = {
            "cv": state["cv"],
            "skills_and_description_list" : state["skills_needed"]
        }

        result = self.template(
            pydantic_obj= SkillsMissingResponse,
            prompt = prompt,
            prompt_value_dict = prompt_value_dict
        )
        
        skills_needed = []
        
        for i in state["skills_needed"]:
            skills_needed.append(i.skill)

        for i in skills_needed:
            if i not in skills_needed :
                error_prompt = ("system", "You have listed skills that is not present in the skills needed list. Please rectify them.")
                prompt_tuple.append(error_prompt)
                temp = prompt_tuple[0]
                prompt_tuple[0] = prompt_tuple[-1]
                prompt_tuple[-1] = temp
                prompt = ChatPromptTemplate.from_messages(prompt_tuple)

                result = self.template(
                                        pydantic_obj= SkillsMissingResponse,
                                        prompt = prompt,
                                        prompt_value_dict = prompt_value_dict
                )
                

        return {
            "skills_missing": result.skills_missing
        }
                                                                  
