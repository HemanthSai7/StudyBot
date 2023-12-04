from pydantic import BaseModel


class FrontendResponseModel(BaseModel):
    message: str
    result: dict
