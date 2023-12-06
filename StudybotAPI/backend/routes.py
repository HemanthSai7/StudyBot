import os
import shutil
from pathlib import Path
from typing import Callable
from tempfile import NamedTemporaryFile

from fastapi import Request, BackgroundTasks
from fastapi import UploadFile
from fastapi.middleware.cors import CORSMiddleware

from backend import app
from backend.schemas import *
from backend.retriever import *
from backend.utils import *


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


@app.post("/api/upload", summary="Upload", tags=["Resource Server"])
def upload_data(bg_tasks: BackgroundTasks, file: UploadFile = File(...)):
    try:
        suffix = Path(file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = os.path.join(os.getcwd(), tmp.name)
    except Exception as e:
        return e
    finally:
        file.file.close()

    # path = os.path.join(os.getcwd(), file.filename)

    bg_tasks.add_task(llm_chain_loader, DATA_PATH=tmp_path)


@app.post("/api/inference",summary="Inference",response_model=FrontendResponseModel,tags=["Resource Server"])
def inference(data: Chat):
    response_result = {
        "message": "success", 
        "result": {}
    }

    ops_inference(response_result, data.promptMessage)
    return response_result
