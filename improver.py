from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import MessagesState
from langgraph.graph import START,END, StateGraph
from langchain_cohere import ChatCohere
import os
from dotenv import load_dotenv
import regex as re
from resources import cv, jd
from prompts import prompts
import streamlit as st

load_dotenv()
os.defpath("myenv/")
key = os.getenv("COHERE_API_KEY")

llm = ChatCohere(cohere_api_key=key, temperature= 0.1)

class state(MessagesState):
    cv : str
    job_description : str
    keywords : str
    score : int
    suggestions : str

attempts = 0
max_attempts = 3

generater_messages = ChatPromptTemplate.from_messages([
   ("system", prompts["generater system prompt"]),
   MessagesPlaceholder("history")
])

generater_human_message = ChatPromptTemplate.from_messages([
    ("human", prompts["generater human message prompt"])
])

evaluater_messages = ChatPromptTemplate.from_messages([
    ("system",prompts["evaluater system message prompt"]),
    MessagesPlaceholder("history")
])

evaluater_human_message = ChatPromptTemplate.from_messages([
    ("human", prompts["evaluater human message prompt"])
])

#Generater node

def generater(state : state):
    global generater_human_message,generater_messages
    print("These are the values in generater")
    print("keyword : ", state["keywords"])
    print("suggestions : ", state["suggestions"])
    generater_human_prompt = generater_human_message.invoke(
        {
            "base_cv": state["cv"], 
            "job_description": state["job_description"], 
            "keywords": state["keywords"], 
            "suggestions": state["suggestions"]
        }
    )

    state["messages"] = generater_human_prompt.messages
    gprompt = generater_messages.invoke({"history": state["messages"]})
    response = llm.invoke(gprompt)
    temp = response

    pattern = r"cv : ((.|\n)+)"
    match = re.search(pattern, temp.content)

    if match:
        state["cv"] = match.group(1)

    return {"cv" : state["cv"]}

#Evaluater node

def evaluater(state : state):
    global evaluater_human_message, evaluater_messages

    evaluater_human_prompt = evaluater_human_message.invoke(
        {
            "cv": state["cv"], 
            "job_description": state["job_description"]
        }
    )

    state["messages"] = evaluater_human_prompt.messages
    eprompt = evaluater_messages.invoke({"history": state["messages"]})
    response = llm.invoke(eprompt)
    temp = response

    pattern = r"score.*?(\d+)"
    match = re.search(pattern, temp.content.lower())

    if match:
        print("matched")
        state["score"] = int(match.group(1))

    pattern = r"(?<=suggestions :\n)((?:- .*\n?)+)"
    match = re.search(pattern, temp.content.lower())

    if match:
        state["suggestions"] = match.group(1)

    pattern = r"(?<=missing keywords :\n)((?:- .*\n?)+)"
    match = re.search(pattern, temp.content.lower())

    if match:
        state["keywords"] = match.group(1)

    print("score now : ", state["score"])

    print("These are the values in evaluater")
    print("keyword : ", state["keywords"])
    print("suggestions : ", state["suggestions"])

    return_dict = {
        "messages" : response, 
        "score" : int(state["score"]), 
        "keywords" : state["keywords"], 
        "suggestions" : state["suggestions"]
    }

    return return_dict

#decider function
def decide_node(state: state):
    global attempts, max_attempts

    attempts += 1
    score = state["score"]
    
    if score >= 90 or attempts == max_attempts:
        st.markdown(state["cv"])
        return END
    else:
        return "generater"

#graph structure

graph = StateGraph(state)

graph.add_node("generater", generater)
graph.add_node("evaluater", evaluater)
graph.add_edge(START, "generater")
graph.add_edge("generater", "evaluater")
graph.add_conditional_edges("evaluater", decide_node)

compiled_graph = graph.compile()

#getting user input

user_input_cv = st.text_input("Your CV")
user_input_jd = st.text_input("Job description")

if user_input_cv and user_input_jd :

    messages = compiled_graph.invoke(
        {
            "messages": "", 
            "cv": user_input_cv,  
            "job_description": user_input_jd, 
            "keywords": "",
            "suggestions" : "", 
            "score": 0
        }
    )




              