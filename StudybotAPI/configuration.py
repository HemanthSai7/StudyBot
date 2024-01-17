"""Configuration for the LLM Apps Course"""
from types import SimpleNamespace

TEAM = "hemanthsai7"
PROJECT = "studybot"
JOB_TYPE = "production"

default_config = SimpleNamespace(
    project=PROJECT,
    entity=TEAM,
    job_type=JOB_TYPE,
    chunk_size=1000,
    chunk_overlap=100,
    num_results=3,
    embeddings="BAAI/llm-embedder",
    vector_DB=".hemanthsai7/studybot/vector_store",
    vector_store_artifact="hemanthsai7/studybot/vector_store:latest",
    normalize_embeddings=True,
    device="cpu",
    vector_space="cosine",
    cache_folder="./cache"
)