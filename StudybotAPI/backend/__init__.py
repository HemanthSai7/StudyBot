import os
import box
import yaml

from fastapi import FastAPI

from backend.ingestion import *

# from langchain.llms.huggingface_pipeline import HuggingFacePipeline


app = FastAPI(title="StudyBot API", version="0.1.0", description="API for StudyBot Project")

from backend import routes
# from backend.retriever import EmbeddingModel


try:
    os.environ["TRANSFORMERS_CACHE"] = "/.cache"

    with open("config.yml", "r", encoding="utf8") as ymlfile:
        cfg = box.Box(yaml.safe_load(ymlfile))
    app.state.emb = Embeddings(cfg) 

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

except Exception as e:
    print(e)
