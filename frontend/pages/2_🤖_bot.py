import requests

import streamlit as st

from layouts.mainlayout import mainlayout
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory

from components.file_streaming import *


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

uploaded_files = st.sidebar.file_uploader(label="Upload PDF files", type=["pdf"])

if not uploaded_files:
    st.info("Please upload PDF documents to continue.")
    st.stop()
upload_data(uploaded_files)

msgs = StreamlitChatMessageHistory()

if len(msgs.messages) == 0 or st.sidebar.button("Clear message history"):
    msgs.clear()
    msgs.add_ai_message("How can I help you?")

avatars = {"human": "user", "ai": "assistant"}
for msg in msgs.messages:
    st.chat_message(avatars[msg.type]).write(msg.content)

if user_query := st.chat_input(placeholder="Ask me anything!"):
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        retrieval_handler = PrintRetrievalHandler(st.container())
        stream_handler = StreamHandler(st.empty())
        response = requests.post(
            "http://127.0.0.1:8000/api/inference",
            json={"promptMessage": user_query},
        ).json()
