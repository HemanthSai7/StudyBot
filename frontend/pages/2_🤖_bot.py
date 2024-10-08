import time
import requests
import streamlit as st

from components.display import *
from layouts.mainlayout import mainlayout
from components.file_streaming import upload_data

from config import default_config

@mainlayout
def display():
    with st.expander("What happens when I upload a PDF? 📑", expanded=True):
        st.info(
            """
            - The PDF is uploaded to the backend server. ⚙️

            - The PDF is converted into small chunks for  faster processing. 🚀
            
            - The chunks are broken down into tokens. A token is a single word or a group of words. 📝

            - The tokens are converted into embedding vectors. 📊

            - The embedding vectors are stored in a vector store. 🗄️
            """,
            icon="ℹ️",
        )

    st.divider()


display()

BASE_URL = default_config.BASE_URL
uploaded_files = st.sidebar.file_uploader(label="Upload PDF files", type=["pdf"])

if not uploaded_files:
    st.info("Please upload PDF documents to continue.")
    st.stop()
upload_data(uploaded_files, BASE_URL)


if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "What's troubling you? Ask me a question right away!",
        }
    ]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


def clear_chat_history():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "What's troubling you? Ask me a question right away!",
        }
    ]


st.sidebar.button("Clear Chat History", on_click=clear_chat_history)


def generate_mistral_response(question: str):
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            question = dict_message["content"]
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/inference",
        json={"promptMessage": question}).json()

        if response["status"]=="error":
            st.error("Please refresh the page and try uploading the file again.")
            st.stop()

        answer = response["result"]["answer"]

        with st.expander("Source documents 🧐"):
            source_documents = response["result"]["source_documents"]
            display_source_document(source_documents)

    except Exception as e:
        if response.json()=='exception.ModelDeployingException()':
            st.error("Model is deploying in the backend servers. Please try again after some time")
            st.stop()

    return answer


def stream_response(prompt):
    for word in prompt.split(" "):
        yield word + " "
        time.sleep(0.02)

# User-provided prompt
if prompt := st.chat_input(
    disabled=not st.session_state.messages[-1]["role"] == "assistant",
    placeholder="Hello, please ask me a question! 🤖"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write_stream(stream_response(prompt))

# ask question
# st.write(st.session_state)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_mistral_response(prompt)
            placeholder = st.empty()
            full_response = ""
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
