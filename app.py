import os
from nodes import nodes
from langgraph.graph import MessagesState
from langgraph.graph import START,END, StateGraph
from resources import cv, jd
from typing import List
import time

node = nodes()

class state(MessagesState):
    cv : str
    job_description : str
    missing_keywords : dict
    missing_aspects : dict
    score : int
    skills_needed : List[dict]
    skills_missing : List[dict]
    

graph = StateGraph(state)

#graph.add_node("keywords_extractor", node.missing_keywords)
#graph.add_node("critic", node.critic)
#graph.add_node("scorer", node.score_calculator)
graph.add_node("skills_missing_generater", node.skills_missing)
graph.add_node("skills_needed_generater", node.skills_needed)

#graph.add_edge(START, "keywords_extractor")
#graph.add_edge(START, "critic")
#graph.add_edge(START,"scorer")
#graph.add_edge(START,"skills_present_generater")
graph.add_edge(START, "skills_needed_generater")
graph.add_edge("skills_needed_generater", "skills_missing_generater")
#graph.add_edge("keywords_extractor", END)
#graph.add_edge("critic", END)
#graph.add_edge("scorer", END)
#graph.add_edge("skills_present_generater", END)
graph.add_edge("skills_missing_generater", END)

compiled_graph = graph.compile()

messages = compiled_graph.invoke(
        {
            "cv": cv,  
            "job_description": jd, 
            "missing_keywords": {},
            "missing_aspects": {},
            "score" : 0,
            "skills_needed" : {},
            "skills_missing" : {}
        }
    )

messages["skills_needed"]
messages["skills_missing"]