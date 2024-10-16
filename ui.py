from rag import create_chain
from app import create_app, stream_output_to_streamlit
from document_loader import load_documents_into_database
from langchain_ollama import ChatOllama
import streamlit as st
import os

st.session_state["llm"] = ChatOllama(model="llama3.1")

PATH = "Document"


st.title("Chatbot with LLM and RAG 🤖")


# Folder selection
folder_path = st.sidebar.text_input("Enter the folder path:", PATH)

if folder_path:
    if not os.path.isdir(folder_path):
        st.error(
            "The provided path is not a valid directory. Please enter a valid folder path."
        )
    else:
        if st.sidebar.button("Index Documents"):
            if "db" not in st.session_state:
                with st.spinner(
                    "Creating embeddings and loading documents into Chroma..."
                ):
                    st.session_state["db"] = load_documents_into_database(
                        folder_path
                    )
                    st.session_state["chain"] = create_chain(db=st.session_state["db"], llm=st.session_state["llm"])
                    st.session_state["app"] = create_app(st.session_state["chain"])
                    st.session_state["config"] = {"configurable": {"thread_id": "abc211"}}
                
                st.info("All set to answer questions!")
else:
    st.warning("Please enter a folder path to load documents into the database.")
   


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        response = stream_output_to_streamlit(prompt, st.session_state["app"], st.session_state["config"])
        st.session_state.messages.append({"role": "assistant", "content": response})
