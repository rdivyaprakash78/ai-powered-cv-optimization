# imports
from langgraph.graph import MessagesState
from nodes import nodes
from resources import cv, jd
from langgraph.graph import START,END, StateGraph
from rich.console import Console
from rich.markdown import Markdown
from typing import List

# state variable class
class state(MessagesState):
    cv : str
    job_description : str
    technical_keywords : List[str]
    non_technical_keywords : List[str]
    score : int
    suggestions : str

node = nodes()

# Graph building

graph = StateGraph(state)
graph.add_node("keywords_extractor", node.keywords_extracting_agent)
graph.add_edge(START, "keywords_extractor")
graph.add_edge("keywords_extractor", END)

compiled_graph = graph.compile()

messages = compiled_graph.invoke(
        {
            "cv": cv,  
            "job_description": jd, 
            "technical_keywords" : [],
            "non_technical_keywords" : [],
            "score" : 0,
            "suggestions" : ""
        }
    )

print("technical_keywords : ", messages["technical_keywords"])
print("non_technical_keywords : ", messages["non_technical_keywords"])





















