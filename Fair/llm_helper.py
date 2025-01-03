from langgraph.graph import MessagesState
from langgraph.graph import START, END, StateGraph
from nodes import nodes

class state(MessagesState):
    attributes : list[dict]

def initiate_graph(jd):

    node = nodes(jd = jd)
    # graph initialisation
    graph = StateGraph(state)
    # nodes defnitions
    graph.add_node("attributes_generator", node.attributes_generator)
    #edges definitions
    graph.add_edge(START, "attributes_generator")
    graph.add_edge("attributes_generator", END)
    #graph compilation
    compiled_graph = graph.compile()

    result = compiled_graph.invoke({
            "attributes" : {}
        })
    
    return result["attributes"]["args"]["attributes"]
    