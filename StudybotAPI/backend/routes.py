from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

from backend import app
from backend.schemas import *
from backend.retriever import *


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Home"])
def api_home():
    return {"detail": "Welcome to Studybot API"}

@app.post("/api/inference", summary="Inference", response_model=Inference, tags=["Resource Server"])
def inference(data: Chat):
    output = ops_inference(data.promptMessage)
    return output
