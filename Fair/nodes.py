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

class Question(BaseModel):
    question : str = Field(description = "The question to be asked to the candidate")
    evaluation_criteria : str = Field(description = "What is the answer expected out of the candidate for this question?")

class SkillMap(BaseModel):
    attribute : str = Field(description = "Missing attribute")
    confidence : int = Field(description = "A confidence score between 0 and 100 of proficiency of that attribute in the candidate")
    description : str = Field(description = "A description of why the attribute is missing")
    priority : int = Field(description = "The priority of the attribute with respect to job description")

class SkillMaps(BaseModel):
    missing_attributes : list[SkillMap] = Field(description = "List of missing attributes along with its corresponding description and confidence")

class nodes :
    def __init__(self, jd, cv):
        self.llm = ChatOpenAI(model = "gpt-4o")
        self.jd = jd
        self.cv = cv

    def template(self, prompt_tuple, prompt_value_dict, pydantic_obj = None):
        prompt = ChatPromptTemplate.from_messages(prompt_tuple)
        if pydantic_obj: 
            llm_with_tools = self.llm.bind_tools([pydantic_obj],strict=True)

        chain = prompt | llm_with_tools
        response = chain.invoke(prompt_value_dict) 

        try :
            return_value = response.tool_calls[0]
        except IndexError:
            return "Technical error occured try again"

        return return_value   
    
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
    
    def skill_mapper(self, state):

        attributes = state["attributes"]["args"]["attributes"]

        system_message = prompts["skill mapper"]["system"]
        human_message = prompts["skill mapper"]["human"]

        prompt_tuple = [
                ("system", system_message),
                ("human", human_message)
            ]
        
        prompt_value_dict = {
                "attributes" : attributes,
                "cv" : self.cv
            }
        
        result = self.template(
                pydantic_obj= SkillMaps,
                prompt_tuple = prompt_tuple,
                prompt_value_dict = prompt_value_dict
            )

        return {
            "skill_map" : result,
        }    

    def question_generator(self, state):

        attributes = state["skill_map"]["args"]["missing_attributes"]
        attributes = sorted(attributes, key=lambda att: att["priority"], reverse=True)
        attributes_to_test = [obj for obj in attributes if obj["confidence"] < 80]
        current_attribute = attributes_to_test[0]["attribute"]

        system_message = prompts["question_generator"]["system"]
        human_message = prompts["question_generator"]["human"]

        prompt_tuple = [
                ("system", system_message),
                ("human", human_message)
            ]
        
        prompt_value_dict = {
                "attribute": attributes_to_test[0]["attribute"],
                "missing" : attributes_to_test[0]["description"]
            }
        
        result = self.template(
                pydantic_obj= Question,
                prompt_tuple = prompt_tuple,
                prompt_value_dict = prompt_value_dict
            )

        ques = result
        history = state["history"]
        history.append(ques)

        return {
            "question" : ques,
            "history": history,
            "skill_map" : attributes,
            "current_attribute" : current_attribute
        } 

    def attribute_updater(self, state):
        answer = state["answer"]

        def create_index(data, key):
            index_map = {}
            for i, obj in enumerate(data):
                index_map[obj[key]] = i
            return index_map

        # Function to pop an object based on key-value pair efficiently
        def pop_by_key_value(data, key, value):
            # Create an index based on the key-value pair
            index_map = create_index(data, key)
            
            # Check if the value exists in the index map
            if value in index_map:
                index = index_map[value]
                popped_object = data.pop(index)
                return popped_object, data
            else:
                return None, data  # If no object with the matching key-value pair is found
            
        popped_object, updated_data = pop_by_key_value(state["skill_map"], "attribute", state["current_attribute"])

        print("popped object : ", popped_object)
        print("updated data : ", updated_data)

        pass
                                         
