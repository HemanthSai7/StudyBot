from backend.schemas import *

from backend import app


def ops_inference(question: str):
    llm_response = app.state.qa_chain(question)
    output = Inference(
        result=llm_response["result"].strip(),
        source_documents=llm_response["source_documents"],
    )
    return output
