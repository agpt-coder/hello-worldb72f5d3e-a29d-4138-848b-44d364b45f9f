from pydantic import BaseModel


class HelloWorldRequestModel(BaseModel):
    """
    Request model for the GET /hello endpoint. No parameters are needed for this request.
    """

    pass


class HelloWorldResponseModel(BaseModel):
    """
    Response model for the GET /hello endpoint. This model contains a single field with the message 'Hello, World!'.
    """

    message: str


def getHelloWorld(request: HelloWorldRequestModel) -> HelloWorldResponseModel:
    """
    This endpoint returns a simple 'Hello, World!' message. When a GET request is made to this endpoint, the server responds
    with a plain text message saying 'Hello, World!'. This is primarily used to test server connectivity and response handling.
    No additional processing or data is required to be passed with the request.

    Args:
        request (HelloWorldRequestModel): Request model for the GET /hello endpoint. No parameters are needed for this request.

    Returns:
        HelloWorldResponseModel: Response model for the GET /hello endpoint. This model contains a single field with the message
        'Hello, World!'.

    Example:
        request = HelloWorldRequestModel()
        response = getHelloWorld(request)
        print(response.message)  # Output: Hello, World!
    """
    return HelloWorldResponseModel(message="Hello, World!")
