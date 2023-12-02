"""Config class for handling env variables.
"""
from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    QDRANT_API_KEY: str
    APP_ID: str
    USER_ID: str
    MODEL_ID: str
    CLARIFAI_PAT: str
    MODEL_VERSION_ID: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


config = get_settings()
