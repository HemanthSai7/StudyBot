import streamlit as st

import requests

# from studybot import qa_chain
# st.write(qa_chain)

upload_pdf = st.file_uploader("Upload PDF", type="pdf")
if upload_pdf is not None:
    files = {"file": upload_pdf}
    response = requests.post(
        "https://hemanthsai7-studybotapi.hf.space/api/upload", files=files
    )
    st.write(response)

query = st.text_input("Question", key="question")
st.write(st.session_state)

if st.button("Ask"):
    # answer = qa_chain(query)
    answer = requests.post(
        "https://hemanthsai7-studybotapi.hf.space/api/inference",
        json={"promptMessage": query},
    ).json()
    st.write(answer)
    # st.session_state["question"] = ""
