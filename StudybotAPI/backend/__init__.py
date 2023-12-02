import os
import box
import yaml

from fastapi import FastAPI

from backend.ingestion import *
from backend.core.configEnv import config

from langchain.prompts import PromptTemplate
from langchain.chains import (
    LLMChain,
    SimpleSequentialChain,
    RetrievalQA,
    ConversationalRetrievalChain,
)
from langchain.llms import LlamaCpp
from langchain.llms import CTransformers
from langchain.llms import Clarifai
# from langchain.llms.huggingface_pipeline import HuggingFacePipeline


app = FastAPI(
    title="StudyBot API", version="0.1.0", description="API for StudyBot Project"
)

from backend import routes
# from backend.retriever import EmbeddingModel


try:
    os.environ["TRANSFORMERS_HOME"] = "backend/.cache"

    with open("config.yml", "r", encoding="utf8") as ymlfile:
        cfg = box.Box(yaml.safe_load(ymlfile))
    emb = Embeddings(cfg)

    docs = PDFDataLoader(cfg.DATA_PATH).load()
    db = emb.store_embeddings(docs)

    with open("backend/prompt.txt", "r", encoding="utf8") as f:
        prompt = f.read()

    prompt = PromptTemplate(template=prompt, input_variables=["context", "question"])

    # llm = HuggingFacePipeline(pipeline=EmbeddingModel._initialize_pipeline())
    # llm = LlamaCpp(
    #     streaming=True,
    #     model_path="models/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    #     max_tokens=1500,
    #     temperature=0.4,
    #     top_p=1,
    #     gpu_layers=0,
    #     stream=True,
    #     verbose=False,
    #     n_threads=int(os.cpu_count() / 2),
    #     n_ctx=4096
    # )

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

except Exception as e:
    print(e)
