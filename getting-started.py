import os
from langchain_groq import ChatGroq

os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"]="getting-started"



prompt = "Hey there."
llm  = ChatGroq(model = "llama-3.3-70b-versatile", temperature=0.25)

result = llm.invoke(prompt)

result.content

from langgraph.graph import START,END, StateGraph
from langgraph.graph import MessagesState

class state(MessagesState):
    result : str

def state_one(state : state):
    prompt = "Your response should be 'I'm in state 1'"
    response = llm.invoke(prompt)
    return {"result" : response}

def state_two(state : state):
    prompt = "Your response should be 'I'm in state 2'"
    response = llm.invoke(prompt)
    return {"result" : response}

graph = StateGraph(state)

graph.add_node("state_one", state_one)
graph.add_node("state_two", state_two)
graph.add_edge(START, "state_one")
graph.add_edge("state_one", "state_two")
graph.add_edge("state_two", END)

compiled_graph = graph.compile()

messages = compiled_graph.invoke({
    "result" : "No state"
})

messages["result"]
