from backend.ingestion import *
from backend import app
from backend.core.configEnv import config

from langchain.chains import (
    LLMChain,
    SimpleSequentialChain,
    RetrievalQA,
    ConversationalRetrievalChain,
)
from langchain.llms import Clarifai
from langchain.prompts import PromptTemplate


def llm_chain_loader(DATA_PATH: str):
    docs = PDFDataLoader(DATA_PATH).load()
    db = app.state.emb.store_embeddings(docs)

    with open("backend/utils/prompt.txt", "r", encoding="utf8") as f:
        prompt = f.read()

    prompt = PromptTemplate(template=prompt, input_variables=["context", "question"])

    llm = Clarifai(
        pat=config.CLARIFAI_PAT,
        user_id=config.USER_ID,
        app_id=config.APP_ID,
        model_id=config.MODEL_ID,
        model_version_id=config.MODEL_VERSION_ID,
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(search_kwargs={"k": 2}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt},
    )

    app.state.qa_chain = qa_chain
