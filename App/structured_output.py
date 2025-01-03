from pydantic import BaseModel, Field
from typing import List
from langchain_core.prompts import ChatPromptTemplate

class MonthYear(BaseModel):
    month : str = Field(description="The month of the year")
    year : str = Field(description="The year of the month")

class Education(BaseModel):
    degree : str = Field(description="Name of the degree")
    institute : str = Field(description="The institute of the degree")
    year : MonthYear = Field(description="The year of graduation")

class WorkExperience(BaseModel):
    company : str = Field(description="The company name")
    role : str = Field(description="The role")
    description : str = Field(description="The description of the roles and responsibilities")
    start_date : str = Field(description="The start date of the job")
    end_date : str = Field(description="The end date of the job")

class Project(BaseModel):
    name : str = Field(description="The name of the project")
    description : str = Field(description="The description of the project")

class Courses(BaseModel):
    name : str = Field(description= "Name of additional courses other than degree")
    description : str = Field(description="Description of additional courses")

class Certifications(BaseModel):
    name : str = Field(description="The name of the certification")
    description : str = Field(description="Short description on the certification")

class CV(BaseModel) :
    name : str = Field( description="The name of the person")
    email : str = Field( description="The email of the person")
    phone : str = Field( description="The phone number of the person")
    location : str = Field( description="The location of the person")
    education :List[Education] = Field( description="The education of the person")
    work_experience : List[WorkExperience] = Field( description="The work experience of the person")
    skills : List[str] = Field( description="The skills of the person")
    projects : List[Project] = Field(description="The projects of the person")
    courses : List[Courses] = Field( description="The additional courses other than degree")
    certifications : List[Certifications] = Field( description="The certifications of the person")

def get_structured_output(text, llm):
    llm_with_tools = llm.bind_tools([CV],strict=True)

    prompt_tuple = [
    ("system", "You are an CV parsing agent. Given a CV you will parse the CV into different fields."),
    ("human", "Here's my CV: {cv}")
    ]

    values_dict = {"cv": text }

    prompt = ChatPromptTemplate.from_messages(prompt_tuple)
    chain = prompt | llm_with_tools
    response = chain.invoke(values_dict)

    return response.tool_calls[0]

