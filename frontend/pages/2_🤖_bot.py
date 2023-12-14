import streamlit as st

from layouts.mainlayout import mainlayout

@mainlayout
def bot():
    st.subheader("Revise your subjects with Studybot!")

bot()