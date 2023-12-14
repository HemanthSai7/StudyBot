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


@app.post("/api/upload", response_model=DataResponseModel,summary="Upload", tags=["Resource Server"])
async def upload_data(file: UploadFile = File(...)):

    response_result = {
        "status": "success",
        "message": ["Data uploaded successfully."]
    }

    try:
        suffix = Path(file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = os.path.join(os.getcwd(), tmp.name)
    except Exception as e:
        response_result["status"] = "error"
        response_result["message"][0]=str(e)
        raise DataNotUploadedException(response_result)
    
    finally:
        file.file.close()

    await llm_chain_loader(DATA_PATH=tmp_path)
    return response_result


@app.post("/api/inference",summary="Inference",response_model=FrontendResponseModel,tags=["Resource Server"])
def inference(data: Chat):
    response_result = {
        "status": "success",
        "message": [""], 
        "result": {}
    }

    ops_inference(response_result, data.promptMessage)
    return response_result
