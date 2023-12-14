from backend.schemas import FrontendResponseModel


class ModelDeploymentException(Exception):
    def __init__(self, response_result: FrontendResponseModel):
        self.response_result = response_result
        self.set_status()
        super(ModelDeploymentException, self).__init__()

    def set_status(self):
        self.response_result["status"] = "Error"
        self.response_result["message"][0]="Model is deploying. Please try again later."

    def __repr__(self):
        return f"exception.ModelDeployingException()"
    


class InfoNotProvidedException(Exception):
    def __init__(self, response_result: FrontendResponseModel, message: str):
        self.response_result = response_result
        self.message = message
        self.set_status()
        super(InfoNotProvidedException, self).__init__(message)

    def set_status(self):
        self.response_result["status"] = "Error"
        self.response_result["message"][0] = "Information not provided."
        self.response_result["message"].append(self.message)

    def __repr__(self):
        return f"exception.InfoNotProvidedException()"


class DataNotUploadedException(Exception):
    def __init__(self, response_result: FrontendResponseModel):
        self.response_result = response_result
        self.set_status()
        super(ModelDeploymentException, self).__init__()

    def set_status(self):
        self.response_result["status"] = "Error"
        self.response_result["message"].append(
            "Data not uploaded. Please upload a file."
        )

    def __repr__(self):
        return f"exception.DataNotUploadedException()"