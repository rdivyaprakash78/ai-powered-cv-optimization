import os
from Fair.nodes import nodes
from langgraph.graph import MessagesState
from langgraph.graph import START,END, StateGraph
from Fair.resources import cv, jd,cv1,cv3
from typing import List
import time

node = nodes()

class state(MessagesState):
    cv : str
    job_description : str
    skills_missing : List[dict]
    skills_present : List[dict]
    question : str
    

graph = StateGraph(state)

graph.add_node("skills_analyzer", node.skills_analyzer)
graph.add_node("question_generator", node.question_generator)
graph.add_edge(START, "skills_analyzer")
graph.add_edge("skills_analyzer", "question_generator")
graph.add_edge("question_generator", END)

compiled_graph = graph.compile()

messages = compiled_graph.invoke(
        {
            "cv": cv3,  
            "job_description": jd, 
            "skills_missing" : {},
            "skills_present" : {},
            "question" : ""
        }
    )

messages["question"]