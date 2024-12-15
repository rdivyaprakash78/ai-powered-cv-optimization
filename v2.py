# imports
from langgraph.graph import MessagesState
from nodes import nodes
from resources import cv, jd
from langgraph.graph import START,END, StateGraph
from rich.console import Console
from rich.markdown import Markdown

# state variable class
class state(MessagesState):
    cv : str
    job_description : str
    keywords : str
    score : int
    suggestions : str

node = nodes()

# Graph building
graph = StateGraph(state)
graph.add_node("generater", node.generater)
graph.add_edge(START, "generater")
graph.add_edge("generater", END)

compiled_graph = graph.compile()

# Initial values for the graph
messages = compiled_graph.invoke(
        {
            "cv" : cv, 
            "job_description" : jd, 
            "keywords" : "", 
            "score" : 0, 
            "suggestions" : ""
        }
)

# Pretty printing
console = Console()
md = Markdown(messages["cv"])
console.print(md)


















