"""Configuration for StudyBot"""
from types import SimpleNamespace

default_config = SimpleNamespace(
    chunk_size=1000,
    chunk_overlap=100,
    num_results=3,
    EMBEDDINGS="BAAI/llm-embedder",
    VECTOR_DB=".hemanthsai7/studybot/vector_store",
    NORMALIZE_EMBEDDINGS=True,
    DEVICE="cpu",
    vector_space="cosine",
    cache_folder="./cache"
)
