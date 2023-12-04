from backend.schemas import *

from backend import app


def ops_inference(response_result: FrontendResponseModel, question: str):
    response_result = {
        "message": "success",
        "result": {}
    }

    try:
        llm_response = app.state.qa_chain(question)
        output = Inference(
            result=llm_response["result"].strip(),
            source_documents=llm_response["source_documents"],
        )
        response_result["result"] = output
    except Exception as e:
        response_result["message"] = "error"
        response_result["result"] = str(e)

