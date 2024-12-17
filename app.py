import os
from nodesv2 import nodes
from langgraph.graph import MessagesState
from langgraph.graph import START,END, StateGraph
from resources import cv, jd

node = nodes()

class state(MessagesState):
    cv : str
    job_decription : str
    missing_keywords : dict
    missing_aspects : dict

graph = StateGraph(state)

graph.add_node("keywords_extractor", node.missing_keywords)
graph.add_node("critic", node.critic)

graph.add_edge(START, "keywords_extractor")
graph.add_edge(START, "critic")
graph.add_edge("keywords_extractor", END)
graph.add_edge("critic", END)

compiled_graph = graph.compile()

messages = compiled_graph.invoke(
        {
            "cv": cv,  
            "job_description": jd, 
            "missing_keywords": {},
            "missing_aspects": {}
        }
    )

messages

for i in messages["missing_aspects"].keys():
    print(i, "\n")
    for j in messages["missing_aspects"][i]:
        print(j)
    print("\n")