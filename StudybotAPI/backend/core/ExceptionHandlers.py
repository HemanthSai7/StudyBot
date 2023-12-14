from backend import app
from .Exceptions import *

from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi import status

@app.exception_handler(ModelDeploymentException)
async def model_deploying_exception_handler(request: Request, exc: ModelDeploymentException):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content=repr(exc)
    )

@app.exception_handler(InfoNotProvidedException)
async def info_not_provided_exception_handler(request: Request, exc: InfoNotProvidedException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=repr(exc)
    )

@app.exception_handler(DataNotUploadedException)
async def data_not_uploaded_exception_handler(request: Request, exc: DataNotUploadedException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=repr(exc)
    )