from pydantic import BaseModel


class HelloWorldRequest(BaseModel):
    """
    Request model for the GET /hello endpoint. There are no parameters required for this request.
    """

    pass


class HelloWorldResponse(BaseModel):
    """
    Response model for the GET /hello endpoint. It contains a simple message indicating 'hello world'.
    """

    message: str


async def helloWorld(request: HelloWorldRequest) -> HelloWorldResponse:
    """
    This endpoint returns a simple 'hello world' message. It does not require any parameters. The response will be a JSON object with a message key.

    Args:
    request (HelloWorldRequest): Request model for the GET /hello endpoint. There are no parameters required for this request.

    Returns:
    HelloWorldResponse: Response model for the GET /hello endpoint. It contains a simple message indicating 'hello world'.

    Example:
        request = HelloWorldRequest()
        response = await helloWorld(request)
        > HelloWorldResponse(message='hello world')
    """
    response = HelloWorldResponse(message="hello world")
    return response
