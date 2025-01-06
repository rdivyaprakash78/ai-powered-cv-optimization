from langgraph.graph import MessagesState
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, END, StateGraph
from nodes import nodes

class state(MessagesState):
    attributes : list[dict]
    history : list[str]
    question : dict
    skill_map : list[dict]
    answer : str
    current_attribute : str

thread = None
compiled_graph = None

def initiate_graph(jd, cv):

    global graph,thread, compiled_graph

    node = nodes(jd = jd, cv = cv)
    # graph initialisation
    graph = StateGraph(state)
    # nodes defnitions
    graph.add_node("attributes_generator", node.attributes_generator)
    graph.add_node("question_generator", node.question_generator)
    graph.add_node("skill_mapper", node.skill_mapper)
    graph.add_node("attribute_updater", node.attribute_updater)
    #edges definitions
    graph.add_edge(START, "attributes_generator")
    graph.add_edge("attributes_generator", "skill_mapper")
    graph.add_edge("skill_mapper", "question_generator")
    graph.add_edge("question_generator", "attribute_updater")
    graph.add_edge("attribute_updater", END)

    memory = MemorySaver()

    #graph compilation
    compiled_graph = graph.compile(interrupt_after=["question_generator"], checkpointer = memory)

    initial_input = {
            "attributes" : {},
            "history" : [],
            "question" : {},
            "skill_map" : {},
            "answer" : "",
            "current_attribute" : ""
        }
    
    thread = {"configurable": {"thread_id": "1"}}

    result = compiled_graph.invoke(initial_input, thread, stream_mode="values")
    return result

def update_graph(answer):

    global graph, thread
    compiled_graph.update_state(thread, {"answer": answer})
    result = compiled_graph.invoke(None, thread, stream_mode="values")

    return result




    