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
    skills_missing : List[dict]
    skills_present : List[dict]
    

graph = StateGraph(state)

#graph.add_node("keywords_extractor", node.missing_keywords)
#graph.add_node("critic", node.critic)
#graph.add_node("scorer", node.score_calculator)
#graph.add_node("skills_missing_generater", node.skills_missing)
graph.add_node("skills_analyzer", node.skills_analyzer)

#graph.add_edge(START, "keywords_extractor")
#graph.add_edge(START, "critic")
#graph.add_edge(START,"scorer")
#graph.add_edge(START,"skills_present_generater")
graph.add_edge(START, "skills_analyzer")
#graph.add_edge("skills_needed_generater", "skills_missing_generater")
#graph.add_edge("keywords_extractor", END)
#graph.add_edge("critic", END)
#graph.add_edge("scorer", END)
#graph.add_edge("skills_present_generater", END)
graph.add_edge("skills_analyzer", END)

compiled_graph = graph.compile()

messages = compiled_graph.invoke(
        {
            "cv": cv,  
            "job_description": jd, 
            "skills_missing" : {},
            "skills_present" : {}
        }
    )

messages["skills_missing"]
messages["skills_present"]