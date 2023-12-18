from backend.schemas import *

from backend.core.Exceptions import *
from backend.core.ExceptionHandlers import *
from backend import app

from clarifai_grpc.grpc.api.status import status_code_pb2

def ops_inference(response_result: FrontendResponseModel, question: str):

    if question == "":
        raise InfoNotProvidedException(response_result, "Come on, I'm not telepathic. I can't read your mind. Please provide me with a question.")

    try:
        llm_response = app.state.qa_chain(question)
        output = Inference(
            answer=llm_response["result"].strip(),
            source_documents=llm_response["source_documents"],
        )

        response_result["result"] = output.dict()
    except Exception as e:
        response_result["status"] = "error"
        response_result["message"].append(str(e))
        print(response_result)
        raise ModelDeploymentException(response_result)