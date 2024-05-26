import logging
from contextlib import asynccontextmanager
from typing import Any, Dict

import prisma
import prisma.enums
import project.create_documentation_service
import project.delete_documentation_service
import project.delete_user_account_service
import project.get_api_documentation_service
import project.get_hello_world_service
import project.get_user_profile_service
import project.getHelloWorld_service
import project.health_check_service
import project.healthCheck_service
import project.helloWorld_service
import project.login_user_service
import project.register_user_service
import project.update_documentation_service
import project.update_user_profile_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="hello world",
    lifespan=lifespan,
    description="create an api that returns just hello world.",
)


@app.put(
    "/api/docs/{docId}",
    response_model=project.update_documentation_service.UpdateAPIDocumentationResponse,
)
async def api_put_update_documentation(
    docId: int,
    endpoint: str,
    method: str,
    description: str,
    request: Dict[str, Any],
    response: Dict[str, Any],
) -> project.update_documentation_service.UpdateAPIDocumentationResponse | Response:
    """
    Updates existing documentation by its id. It is critical to provide accurate and updated descriptions for endpoints.
    """
    try:
        res = project.update_documentation_service.update_documentation(
            docId, endpoint, method, description, request, response
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/health", response_model=project.healthCheck_service.HealthCheckResponse)
async def api_get_healthCheck(
    request: project.healthCheck_service.HealthCheckRequest,
) -> project.healthCheck_service.HealthCheckResponse | Response:
    """
    This endpoint checks the status of the service. It returns a JSON object containing the status of the service to ensure it's running correctly.
    """
    try:
        res = project.healthCheck_service.healthCheck(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/api/user/account",
    response_model=project.delete_user_account_service.DeleteUserAccountResponse,
)
async def api_delete_delete_user_account(
    request: project.delete_user_account_service.DeleteUserAccountRequest,
) -> project.delete_user_account_service.DeleteUserAccountResponse | Response:
    """
    Deletes the authenticated user's account. Requires a valid JWT token. Returns a confirmation message upon successful deletion.
    """
    try:
        res = await project.delete_user_account_service.delete_user_account(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/api/user/profile",
    response_model=project.update_user_profile_service.UpdatedUserProfileResponse,
)
async def api_put_update_user_profile(
    email: str, password: str, role: prisma.enums.Role
) -> project.update_user_profile_service.UpdatedUserProfileResponse | Response:
    """
    Updates the profile of the authenticated user. Requires a valid JWT token. Accepts updated user profile information and returns the updated profile.
    """
    try:
        res = project.update_user_profile_service.update_user_profile(
            email, password, role
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/api/user/profile",
    response_model=project.get_user_profile_service.UserProfileResponse,
)
async def api_get_get_user_profile(
    request: project.get_user_profile_service.GetUserProfileRequest,
) -> project.get_user_profile_service.UserProfileResponse | Response:
    """
    Retrieves the profile of the authenticated user. Requires a valid JWT token. Returns user profile information.
    """
    try:
        res = project.get_user_profile_service.get_user_profile(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/health", response_model=project.health_check_service.HealthCheckResponse)
async def api_get_health_check(
    request: project.health_check_service.HealthCheckInput,
) -> project.health_check_service.HealthCheckResponse | Response:
    """
    This endpoint verifies the operational status of the API. When called, it returns a simple message 'Hello World' indicating the API is operational. It does not interact with any other APIs or databases and should always return a 200 OK status if the service is running.
    """
    try:
        res = project.health_check_service.health_check(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/hello", response_model=project.getHelloWorld_service.HelloWorldResponseModel)
async def api_get_getHelloWorld(
    request: project.getHelloWorld_service.HelloWorldRequestModel,
) -> project.getHelloWorld_service.HelloWorldResponseModel | Response:
    """
    This endpoint returns a simple 'Hello, World!' message. When a GET request is made to this endpoint, the server responds with a plain text message saying 'Hello, World!'. This is primarily used to test server connectivity and response handling. No additional processing or data is required to be passed with the request.
    """
    try:
        res = project.getHelloWorld_service.getHelloWorld(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/api/docs/{docId}",
    response_model=project.delete_documentation_service.DeleteApiDocResponseModel,
)
async def api_delete_delete_documentation(
    docId: int,
) -> project.delete_documentation_service.DeleteApiDocResponseModel | Response:
    """
    Deletes documentation by its id. This removes outdated or incorrect documentation ensuring only relevant information is available.
    """
    try:
        res = await project.delete_documentation_service.delete_documentation(docId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/api/docs", response_model=project.get_api_documentation_service.ApiDocsResponse
)
async def api_get_get_api_documentation(
    request: project.get_api_documentation_service.GetApiDocsRequest,
) -> project.get_api_documentation_service.ApiDocsResponse | Response:
    """
    Fetches the complete API documentation including requests and responses for all available endpoints. This requires consolidating documentation generated by HelloWorldHandler and HealthCheckHandler.
    """
    try:
        res = await project.get_api_documentation_service.get_api_documentation(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/api/register",
    response_model=project.register_user_service.UserRegistrationResponse,
)
async def api_post_register_user(
    username: str, password: str
) -> project.register_user_service.UserRegistrationResponse | Response:
    """
    Creates a new user account. Expects a username and password. If successful, returns a newly created user object.
    """
    try:
        res = await project.register_user_service.register_user(username, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/api/hello-world",
    response_model=project.get_hello_world_service.HelloWorldResponse,
)
async def api_get_get_hello_world(
    request: project.get_hello_world_service.HelloWorldRequest,
) -> project.get_hello_world_service.HelloWorldResponse | Response:
    """
    Returns a 'Hello World' message. Requires the user to be authenticated. Uses JWT token for user verification.
    """
    try:
        res = await project.get_hello_world_service.get_hello_world(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/hello", response_model=project.helloWorld_service.HelloWorldResponse)
async def api_get_helloWorld(
    request: project.helloWorld_service.HelloWorldRequest,
) -> project.helloWorld_service.HelloWorldResponse | Response:
    """
    This endpoint returns a simple 'hello world' message. It does not require any parameters. The response will be a JSON object with a message key.
    """
    try:
        res = await project.helloWorld_service.helloWorld(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/api/login", response_model=project.login_user_service.LoginResponseModel)
async def api_post_login_user(
    username: str, password: str
) -> project.login_user_service.LoginResponseModel | Response:
    """
    Authenticates a user. Expects a username and password, returns a JWT token upon successful authentication.
    """
    try:
        res = await project.login_user_service.login_user(username, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/api/docs",
    response_model=project.create_documentation_service.ApiDocsCreateOrUpdateResponse,
)
async def api_post_create_documentation(
    endpoint: str, method: str, description: str, request: Dict, response: Dict
) -> project.create_documentation_service.ApiDocsCreateOrUpdateResponse | Response:
    """
    Allows an authorized user to create or update API documentation. The payload should include detailed descriptions for new or updated endpoints handled by HelloWorldHandler and HealthCheckHandler.
    """
    try:
        res = await project.create_documentation_service.create_documentation(
            endpoint, method, description, request, response
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
