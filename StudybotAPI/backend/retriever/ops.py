import datetime
from configuration import default_config
from wandb.sdk.data_types.trace_tree import Trace

from backend.schemas import *
from backend.core.Exceptions import *
from backend.core.ExceptionHandlers import *
from backend import app


def ops_inference(response_result: FrontendResponseModel, question: str):
    start_time_ms = datetime.datetime.now().timestamp() * 1000

    if question == "":
        raise InfoNotProvidedException(
            response_result,
            "Come on, I'm not telepathic. I can't read your mind. Please provide me with a question.",
        )

    try:
        llm_response = app.state.qa_chain(question)
        output = Inference(
            answer=llm_response["result"].strip(),
            source_documents=llm_response["source_documents"],
        )

        response_result["result"] = output.dict()

        end_time_ms = round(datetime.datetime.now().timestamp() * 1000)

    except Exception as e:
        end_time_ms = round(datetime.datetime.now().timestamp() * 1000)
        response_result["status"] = "error"
        response_result["message"].append(str(e))
        print(response_result)
        raise ModelDeploymentException(response_result)
    
    root_span = Trace(
        name="inference",
        kind="chain",
        status_code=response_result["status"],
        status_message=response_result["message"],
        metadata={"model_name": "Mistral-7B-instruct",
                  "question": question},
        start_time_ms=start_time_ms,
        end_time_ms=end_time_ms,
        outputs={"result":response_result["result"]}

    )

    root_span.log(name="mistral_trace")
