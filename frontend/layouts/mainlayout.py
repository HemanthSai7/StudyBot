import json
import streamlit as st

import requests

from typing import Callable
from components import authors, user_greetings, add_logo


def mainlayout(func: Callable):
    def wrapper():
        with open("frontend/layouts/st_page_layouts.json", "r", encoding="utf-8") as f:
            st_page_layouts = json.load(f)

        st.set_page_config(
            **st_page_layouts[
                f"{func.__name__}"
                if func.__name__ in st_page_layouts.keys()
                else "home"
            ]
        )
        add_logo("frontend/images/studybotlogo.svg", svg=True)
        st.markdown("# Studybot 📚")
        user_greetings()
        authors()

        func()

    return wrapper
