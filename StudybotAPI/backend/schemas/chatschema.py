from pydantic import BaseModel


class Inference(BaseModel):
    result: str
    source_documents: list


class Chat(BaseModel):
    promptMessage: str
