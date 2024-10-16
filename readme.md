# Chatbot with LLM and RAG
This is an experimental project that utilizes a local Large Language Model ([Llama 3.1](https://ollama.com/library/llama3.1) in this case) to perform Retrieval-Augmented Generation (RAG), enabling it to answer questions based on information extracted from sample PDFs. For embeddings, we are using the [BGE-M3](https://huggingface.co/BAAI/bge-m3) model along with the [Chroma](https://docs.trychroma.com/) VectorStore.

Additionally, a web-based UI has been developed using [Streamlit](https://streamlit.io/) to offer an alternative and user-friendly interface for interacting with the chatbot.

## How to Use

**Note:** Ensure that you have downloaded the [Llama 3.1](https://ollama.com/library/llama3.1) model before proceeding. You can follow the official instructions provided by the model’s source to download and set it up.

1. Before running the project, make sure you have a virtual environment set up and activated.
2. Once the virtual environment is active, install all the necessary dependencies by running:  
    `pip install -r requirements.txt`
3. After installing the dependencies, you can launch the Streamlit-based UI for the chatbot by running the following command:  
    `streamlit run ui.py`

## References
https://python.langchain.com/docs/tutorials/chatbot/
