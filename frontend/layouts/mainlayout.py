import json
import streamlit as st
from typing import Callable
from components import authors, user_greetings


def mainlayout(func: Callable):
    def wrapper():
        with open("frontend/layouts/st_page_layouts.json", "r", encoding="utf-8") as f:
            st_page_layouts = json.load(f)

        st.set_page_config(**st_page_layouts[f"{func.__name__}" if func.__name__ in st_page_layouts.keys() else "home"])
        st.markdown('# :rainbow[Welcome to Studybot]🚀')
        user_greetings()
        authors()

        func()

    return wrapper
