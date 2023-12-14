import streamlit as st

def user_greetings():
    with st.sidebar.expander("👋 Greetings!", expanded=True):
        st.write("Welcome to Studybot! This is a tool to help you revise your subjects. You can use the sidebar to navigate to the different pages. Have fun!")
        st.write("If you have any feedback, please contact me on [LinkedIn](https://www.linkedin.com/in/hemanthsai7/) or [GitHub](https://github.com/HemanthSai7).")