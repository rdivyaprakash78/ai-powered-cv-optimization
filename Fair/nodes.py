import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from prompts import prompts
from pydantic import BaseModel, Field, field_validator
from langchain_openai import ChatOpenAI

load_dotenv()

os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"]="cv-improver"

# Pydantic response model
class Attribute(BaseModel):
    attribute : str = Field(description = "The attribute that is expected by the job recruiter from the candidate")
    priority: int = Field(description = "A score out of 100 to quantify how much important is the attribute for the job")
    description : str = Field(description = "A short description on what the recruiter is expecting from the canddiate regarding the attribute")

    @field_validator('priority')
    def check_priority_range(cls, value):
        if not (0 <= value <= 100):
            raise ValueError('Priority score must be between 0 and 100')
        return value

class Attributes(BaseModel):
    attributes : list[Attribute] = Field(description = "List of all the attributes along with its corresponding priority score and description")

class nodes :
    def __init__(self, jd):
        self.llm = ChatOpenAI(model = "gpt-4o")
        self.jd = jd

    def template(self, prompt_tuple, prompt_value_dict, pydantic_obj = None):
        prompt = ChatPromptTemplate.from_messages(prompt_tuple)
        if pydantic_obj: 
            llm_with_tools = self.llm.bind_tools([pydantic_obj],strict=True)

        chain = prompt | llm_with_tools
        response = chain.invoke(prompt_value_dict) 

        return response.tool_calls[0]    
    
    def attributes_generator(self, state):
        system_message = prompts["attributes_generator"]["system"]
        human_message = prompts["attributes_generator"]["human"]

        prompt_tuple = [
                ("system", system_message),
                ("human", human_message)
            ]
        
        prompt_value_dict = {
                "job_description": self.jd
            }
        
        result = self.template(
                pydantic_obj= Attributes,
                prompt_tuple = prompt_tuple,
                prompt_value_dict = prompt_value_dict
            )
        
        return {
            "attributes" : result
        }                                             
