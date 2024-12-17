import os
from dotenv import load_dotenv
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from prompts import prompts
from langchain_groq import ChatGroq
from langchain_core.exceptions import OutputParserException
from typing import List
from pydantic import BaseModel, Field
from resources import cv,jd

load_dotenv()

os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"]="cv-improver"

class nodes :

    def __init__(self):
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.25)
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

    def missing_keywords (self, state):

        class keywords_extracting_response(BaseModel):
            non_technical_keywords : List[str] = Field(description="List of extracted ATS friendly keywords that are missing in the CV based on the Job description")
            technical_keywords : List[str] = Field(description="List of extracted ATS friendly technical keywords that are missing in the CV based on the Job description")

        prompt = ChatPromptTemplate.from_messages([
            ("system", prompts["keywords extractor system prompt"]),
            ("human", prompts["keywords extractor human prompt"])
        ]
        )

        prompt_value_dict = {
            "cv": cv,
            "job_description": jd
        }

        result = self.template(
            pydantic_obj= keywords_extracting_response,
            prompt = prompt,
            prompt_value_dict = prompt_value_dict
        )

        return {
            "missing_keywords" : {
                "technical" : result.technical_keywords, 
                "non technical" : result.non_technical_keywords
                }
            }
    
    def critic(self, state):

        class CriticResponse(BaseModel):
            technical_aspects : str = Field(description= "Report that describes the technical aspects that are missing in the candidate's CV that the job requires.")
            non_technical_aspects : str = Field(description= "Report that describe the non-technical aspects that are missing in the candidate's CV that the job requires.")

        prompt = ChatPromptTemplate.from_messages([
            ("system", prompts["critic system prompt"]),
            ("human", prompts["critic human prompt"])
        ]
        )

        prompt_value_dict = {
            "cv": cv,
            "job_description": jd
        }

        result = self.template(
            pydantic_obj= CriticResponse,
            prompt = prompt,
            prompt_value_dict = prompt_value_dict
        )

        return {
            "missing_aspects" : {
                "technical" : result.technical_aspects,
                "non technical" : result.non_technical_aspects
            }
        }
    
