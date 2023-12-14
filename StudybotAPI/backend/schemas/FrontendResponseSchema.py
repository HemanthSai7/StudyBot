from typing import List
from pydantic import BaseModel


class FrontendResponseModel(BaseModel):
    status: str
    message: List[str]
    result: dict

class DataResponseModel(BaseModel):
    status: str
    message: List[str]