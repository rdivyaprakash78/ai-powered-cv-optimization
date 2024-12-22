
from pydantic import BaseModel, Field
from typing import List
from langchain_core.prompts import ChatPromptTemplate
import os
from resources import cv3
from langchain_openai import ChatOpenAI


os.environ["OPENAI_API_KEY"] = str(os.environ.get("OPENAI_API_KEY"))

llm = ChatOpenAI(model="gpt-4o", temperature=0)

class Education(BaseModel):
  degree : str = Field(description="The degree of the person")
  institute : str = Field(description="The institute of the person")
  year : str = Field(description="The year of the person")

class WorkExperience(BaseModel):
  company : str = Field(description="The company name")
  role : str = Field(description="The role")
  description : str = Field(description="The description of the roles and responsibilities")
  start_date : str = Field(description="The start date of the job")
  end_date : str = Field(description="The end date of the job")

class CV(BaseModel) :
  name : str = Field(description="The name of the person")
  email : str = Field(description="The email of the person")
  phone : str = Field(description="The phone number of the person")
  location : str = Field(description="The location of the person")
  education : List[Education] = Field(description="The education of the person")
  work_experience : List[WorkExperience] = Field(description="The work experience of the person")
  skills : List[str] = Field(description="The skills of the person")
  projects : List[str] = Field(description="The projects of the person")

llm_with_tools = llm.bind_tools([CV],strict=True)


def get_structured_output(cv):
  
  llm = llm_with_tools

  prompt_tuple = [
    ("system", "You are an CV parsing agent. Given a CV you will parse the CV into different fields."),
    ("human", "Here's my CV: {cv}")
  ]

  values_dict = {"cv": cv }

  prompt = ChatPromptTemplate.from_messages(prompt_tuple)
  chain = prompt | llm
  response = chain.invoke(values_dict)

  return response.tool_calls[0]["args"]







