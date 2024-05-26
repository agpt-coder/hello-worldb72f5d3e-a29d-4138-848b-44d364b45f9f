import jwt
import prisma
import prisma.models
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


async def verify_user(token: str) -> bool:
    """
    Verifies the user's JWT token to ensure they are authenticated.

    Args:
        token (str): The JWT token for user authentication.

    Returns:
        bool: True if the user is authenticated, False otherwise.

    Example:
        token = "some.jwt.token"
        verify_user(token)
        > True
    """
    try:
        decoded_token = jwt.decode(token, "your-secret-key", algorithms=["HS256"])
        user_id = decoded_token.get("user_id")
        if user_id:
            user = await prisma.models.User.prisma().find_unique(
                where={"id": int(user_id)}
            )
            return user is not None
        return False
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False


async def get_hello_world(request: HelloWorldRequest) -> HelloWorldResponse:
    """
    Returns a 'Hello World' message. Requires the user to be authenticated. Uses JWT token for user verification.

    Args:
        request (HelloWorldRequest): Request model for the GET /hello endpoint. There are no parameters required for this request.

    Returns:
        HelloWorldResponse: Response model for the GET /hello endpoint. It contains a simple message indicating 'hello world'.

    Example:
        request = HelloWorldRequest()
        get_hello_world(request)
        > HelloWorldResponse(message='hello world')
    """
    authorization = "Bearer your.jwt.token"
    token = authorization.split("Bearer ")[1]
    if await verify_user(token):
        return HelloWorldResponse(message="hello world")
    else:
        from fastapi import HTTPException

        raise HTTPException(status_code=401, detail="Unauthorized")
