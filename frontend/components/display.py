import streamlit as st


def display_source_document(source_document: list):
    for i, source in enumerate(source_document):
        st.markdown(f"{i+1}. ##### Source content ")

        st.markdown(f'- {source["page_content"]}')

        st.markdown(f'- **Page number:** {source["metadata"]["page"]}')
