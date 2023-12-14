from pydantic import BaseModel
from fastapi import File, UploadFile


class Inference(BaseModel):
    answer: str
    source_documents: list

class Chat(BaseModel):
    promptMessage: str

class Upload(BaseModel):
    file : UploadFile
