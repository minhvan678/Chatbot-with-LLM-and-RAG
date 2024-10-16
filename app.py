import streamlit as st
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict
from typing import Sequence


### Statefully manage chat history ###
class State(TypedDict):
    input: str
    chat_history: Annotated[Sequence[BaseMessage], add_messages]
    context: str
    answer: str

def call_model(state: State, rag_chain):
    response = rag_chain.invoke(state)
    return {
        "chat_history": [
            HumanMessage(state["input"]),
            AIMessage(response["answer"]),
        ],
        "context": response["context"],
        "answer": response["answer"],
    }

def create_app(chain):
    workflow = StateGraph(state_schema=State)
    workflow.add_edge(START, "model")
    
    workflow.add_node("model", lambda state: call_model(state, chain))
    
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)
    return app

def stream_output_to_streamlit(question: str, app, config):
    # Create a placeholder for the output
    output_placeholder = st.empty()
    response = ""  # Initialize an empty response to store the streamed chunks
    
    inputs = {"input": question}

    # Stream the output chunks to the Streamlit UI
    for chunk, metadata in app.stream(inputs, config=config, stream_mode="messages"):
        if isinstance(chunk, AIMessage):  # Check if the chunk is an AI message
            # Append the content to the response
            response += chunk.content
            # Update the Streamlit placeholder with the latest output
            output_placeholder.markdown(response)
    
    return response