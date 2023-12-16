import requests

import streamlit as st

from layouts.mainlayout import mainlayout

@mainlayout
def upload_data():
    # upload pdf
    upload_pdf = st.file_uploader("Upload PDF", type="pdf")
    if upload_pdf is not None:
        files = {"file": upload_pdf}
        with st.spinner("Uploading PDF..."):
            response = requests.post(
                "https://hemanthsai7-studybotapi.hf.space/api/upload", files=files
            )

            if response.status_code == 200:
                st.success(
                    f'{response.json()["message"][0]}. Vector Store created successfully!'
                )
                st.session_state.uploaded_pdf=True
            else:
                st.error("Failed to upload PDF!")

        

upload_data()

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

if "uploaded_pdf" in st.session_state.keys():
    # chatbot
    st.subheader("Ask Studybot a question! 🤖")


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

        answer = requests.post(
            "https://hemanthsai7-studybotapi.hf.space/api/inference",
            json={"promptMessage": question},
        ).json()

        return answer


    # User-provided prompt
    if prompt := st.chat_input(
        disabled=not st.session_state.messages[-1]["role"] == "assistant",
        placeholder="Hello, please ask me a question! 🤖"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # ask question
    st.write(st.session_state)

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
