from datetime import datetime
from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class Question(BaseModel):
    """
    The structure for a question object.
    """

    id: int
    title: str
    content: str
    createdAt: datetime
    updatedAt: datetime


class Answer(BaseModel):
    """
    The structure for an answer object.
    """

    id: int
    content: str
    createdAt: datetime
    updatedAt: datetime


class UserRegistrationResponse(BaseModel):
    """
    This model encapsulates the response for a successful user registration, which includes the newly created user object.
    """

    id: int
    email: str
    role: prisma.enums.Role
    questions: List[Question]
    answers: List[Answer]


async def register_user(username: str, password: str) -> UserRegistrationResponse:
    """
    Creates a new user account. Expects a username and password. If successful, returns a newly created user object.

    Args:
    username (str): The desired username for the new user.
    password (str): The desired password for the new user.

    Returns:
    UserRegistrationResponse: This model encapsulates the response for a successful user registration, which includes the newly created user object.

    Example:
        response = await register_user("newuser", "safe_password")
        print(response)
    """
    new_user = await prisma.models.User.prisma().create(
        data={"email": username, "password": password, "role": "User"}
    )
    registered_user_response = UserRegistrationResponse(
        id=new_user.id,
        email=new_user.email,
        role=new_user.role,
        questions=[],
        answers=[],
    )
    return registered_user_response
