import streamlit as st

# from studybot import qa_chain
# st.write(qa_chain)

query=st.text_input("Question", key="question")
st.write(st.session_state)

if st.button("Ask"):
    # answer = qa_chain(query)
    answer = st.session_state["qa_chain"](query)
    st.write(answer)
    # st.session_state["question"] = ""
