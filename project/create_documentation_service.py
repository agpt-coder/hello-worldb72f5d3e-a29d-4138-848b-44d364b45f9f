from typing import Dict

import prisma
import prisma.models
from pydantic import BaseModel


class ApiDocsCreateOrUpdateResponse(BaseModel):
    """
    The response model for confirming the creation or update of the API documentation.
    """

    message: str
    api_doc_id: int


async def create_documentation(
    endpoint: str, method: str, description: str, request: Dict, response: Dict
) -> ApiDocsCreateOrUpdateResponse:
    """
    Allows an authorized user to create or update API documentation. The payload should include detailed descriptions for new or updated endpoints handled by HelloWorldHandler and HealthCheckHandler.

    Args:
        endpoint (str): The endpoint URL being documented.
        method (str): HTTP method for the endpoint (e.g. GET, POST).
        description (str): A detailed description of what the endpoint does.
        request (Dict): The JSON structure representing the request payload for the endpoint.
        response (Dict): The JSON structure representing the response payload for the endpoint.

    Returns:
        ApiDocsCreateOrUpdateResponse: The response model for confirming the creation or update of the API documentation.

    Example:
        endpoint = "/hello-world"
        method = "GET"
        description = "Returns a simple 'Hello, world!' message."
        request = {}
        response = {"message": "Hello, world!"}
        create_documentation(endpoint, method, description, request, response)
        > ApiDocsCreateOrUpdateResponse(message="Documentation created/updated successfully.", api_doc_id=1)
    """
    existing_doc = await prisma.models.APIDocumentation.prisma().find_first(
        where={"endpoint": endpoint, "method": method}
    )
    if existing_doc:
        updated_doc = await prisma.models.APIDocumentation.prisma().update(
            where={"id": existing_doc.id},
            data={"description": description, "request": request, "response": response},
        )
        return ApiDocsCreateOrUpdateResponse(
            message="Documentation updated successfully.", api_doc_id=updated_doc.id
        )
    else:
        new_doc = await prisma.models.APIDocumentation.prisma().create(
            data={
                "endpoint": endpoint,
                "method": method,
                "description": description,
                "request": request,
                "response": response,
            }
        )
        return ApiDocsCreateOrUpdateResponse(
            message="Documentation created successfully.", api_doc_id=new_doc.id
        )
