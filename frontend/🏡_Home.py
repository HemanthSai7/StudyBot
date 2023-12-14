import streamlit as st

from layouts.mainlayout import mainlayout


@mainlayout
def home():
    st.subheader("Revise your subjects with Studybot!")

    st.markdown(
        """
            <p style='text-align: justify;'>
                <b>Studybot</b> is a <b>free</b> and <b>open-source</b> tool for <b>automated</b> and <b>personalized</b> learning. 
                It is a <b>chatbot</b> that helps you to <b>learn</b> and <b>memorize</b> new information in a <b>fun</b> and <b>easy</b> way.  
                Studybot is <b>free</b> and <b>open-source</b>, so you can use it <b>without any limitations</b> and <b>without any costs</b>. 
                You can also <b>customize</b> it to your needs and <b>contribute</b> to its development. 
                <b>Enjoy</b> your learning with Studybot!
            </p>
            """,
        unsafe_allow_html=True,
    )

    with st.expander("How does it work?", expanded=True):
        st.markdown(
            """
            - When you upload a document, it will be divided into smaller chunks and stored in a special type of database called a vector index that allows for semantic search and retrieval. I'm using Qdrant vector database for this purpose.

            - When you ask a question, Studybot will search through the document chunks and find the most relevant ones using the vector index. Then, it will use Mistral-7B-instruct to generate a final answer.

            """
        )

    with st.expander("FAQs 🤔"):
        st.markdown(
            """
            - **What is the best way to upload a document?**<br>
            The best way to upload a document is to upload a PDF file. Studybot will automatically divide it into smaller chunks. You can also upload a text file. In this case, Studybot will divide it into smaller chunks.

            - **What is the best way to ask questions?**<br>
            The best way to ask questions is to ask questions that are related to the document you uploaded. If you ask questions that are not related to the document you uploaded, Studybot will not be able to answer them.

            - **Is my data safe?**<br>
            Yes, your data is safe. Studybot does not store your documents or questions. All uploaded data is deleted after you close the browser tab since it is stored in the RAM memory. However, if you want to be sure that your data is safe, you can use the `Clear data 🧹` button to delete all uploaded data.

            - **Why does it take so long to index my document?**<br>
            When you upload a document, it is divided into smaller chunks and stored in a special type of database called a vector index that allows for semantic search and retrieval. It takes some time to index your document because it has to be divided into smaller chunks and stored in the vector index. However, once your document is indexed, it will be much faster to search through it.

            - **Are the answers 100% accurate?**<br>
              - No, the answers are not 100% accurate. Studybot uses Mistral-7B to generate answers. Mistral-7B is a powerful language model, but it sometimes makes mistakes and is prone to hallucinations. Also, Studybot uses semantic search to find the most relevant chunks and does not see the entire document, which means that it may not be able to find all the relevant information and may not be able to answer all questions (especially summary-type questions or questions that require a lot of context from the document).

              - But for most of the time, Studybot is very accurate and can answer most questions. Always check with the sources to make sure that the answers are correct.

            - **What is the best way to contribute to Studybot?**<br>
            The best way to contribute to Studybot is to create an issue on GitHub. I will be happy to answer your questions and help you with your contributions.
            """,
            unsafe_allow_html=True,
        )
    
    st.divider()
    # architecture heading in the middle
    st.markdown("<h2 style='text-align: center; color: black;'>Studybot Architecture</h1>", unsafe_allow_html=True)
    st.image("frontend/images/architecture.png")


home()
