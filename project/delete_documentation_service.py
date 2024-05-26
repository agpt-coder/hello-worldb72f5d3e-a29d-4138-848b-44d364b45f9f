import prisma
import prisma.models
from pydantic import BaseModel


class DeleteApiDocResponseModel(BaseModel):
    """
    This response model indicates the successful deletion of the API documentation entry.
    """

    success: bool
    message: str


async def delete_documentation(docId: int) -> DeleteApiDocResponseModel:
    """
    Deletes documentation by its id. This removes outdated or incorrect documentation ensuring only relevant information is available.

    Args:
        docId (int): The unique identifier of the API documentation to be deleted.

    Returns:
        DeleteApiDocResponseModel: This response model indicates the successful deletion of the API documentation entry.

    Example:
        delete_documentation(1)
        > DeleteApiDocResponseModel(success=True, message='API documentation deleted successfully.')
    """
    documentation = await prisma.models.APIDocumentation.prisma().find_unique(
        where={"id": docId}
    )
    if not documentation:
        return DeleteApiDocResponseModel(
            success=False, message="API documentation not found."
        )
    await prisma.models.APIDocumentation.prisma().delete(where={"id": docId})
    return DeleteApiDocResponseModel(
        success=True, message="API documentation deleted successfully."
    )
