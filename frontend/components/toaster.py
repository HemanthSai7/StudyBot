import streamlit as st

import time


def toaster_messages(func: callable):
    def wrapper():
        msg = st.toast("Uploading PDF...")
        time.sleep(8)
        msg.toast("Converting PDF into small chunks...")
        time.sleep(8)
        msg.toast("Breaking down chunks into tokens...")
        time.sleep(8)
        msg.toast("Creating embeddging vectors...")
        time.sleep(8)
        msg.toast("Creating vector store...")
        time.sleep(8)
        msg.toast("Vector store created successfully!")

        func()

    return wrapper
