from backend.ingestion import *
from backend import app
from backend.core.configEnv import config
from configuration import default_config


from langchain.chains import (
    LLMChain,
    SimpleSequentialChain,
    RetrievalQA,
    ConversationalRetrievalChain,
)
from langchain.llms import Clarifai
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.embeddings import HuggingFaceBgeEmbeddings

import wandb

async def data_ingestion(DATA_PATH: str):
    docs = PDFDataLoader(DATA_PATH).load()
    run = wandb.init(project=default_config.project, job_type=default_config.job_type)
    vector_store = app.state.emb.ingest_data(docs)
    app.state.emb.log_dataset(docs, run)
    app.state.emb.log_index(default_config.vector_DB, run)
    run.finish()

    return vector_store
        

def llm_chain_loader(vector_store: Chroma):
    wandb_run = wandb.init(
        project=default_config.project,
        job_type=default_config.job_type,
        entity=default_config.entity,
        config=default_config,
    )

    # load vector store artifact
    vector_store_artifact_dir = wandb_run.use_artifact(
        wandb_run.config.vector_store_artifact, type="search_index"
    ).download()

    embedding_fn = HuggingFaceBgeEmbeddings(
        model_name=default_config.embeddings,
        model_kwargs={"device": default_config.device},
        encode_kwargs={"normalize_embeddings": default_config.normalize_embeddings},
    )

    # load vector store
    vector_store = Chroma(
        embedding_function=embedding_fn, persist_directory=vector_store_artifact_dir
    )
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
        retriever=vector_store.as_retriever(
            search_type="mmr", search_kwargs={"k": 2, "fetch_k": 4}
        ),
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt},
    )

    # memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    # qa_chain = ConversationalRetrievalChain.from_llm(
    #     llm=llm,
    #     chain_type="stuff",
    #     retriever=db.as_retriever(
    #         search_type="mmr", search_kwargs={"k": 2, "fetch_k": 4}),
    #     # return_source_documents=True,
    #     # chain_type_kwargs={"prompt": prompt},
    #     condense_question_prompt=prompt,
    #     memory=memory,
    # )

    app.state.qa_chain = qa_chain
