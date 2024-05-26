from datetime import datetime, timedelta
from typing import Optional

import bcrypt
import jwt
import prisma
import prisma.models
from pydantic import BaseModel


class LoginResponseModel(BaseModel):
    """
    This model returns the JWT token upon successful authentication.
    """

    token: str


SECRET_KEY = "your_secret_key"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against its hashed version.

    Args:
        plain_password (str): The plain text password.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if the password matches, False otherwise.

    Example:
        plain_password = 'secret'
        hashed_password = '$2b$12$EIXIzK9E9Lp5b/r9Q5K9De5GQsL9uZw4qe1kDkNOEeD9OH/xOoG8T'
        verify_password(plain_password, hashed_password)
        > True
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT token.

    Args:
        data (dict): The data to include in the JWT token.
        expires_delta (Optional[timedelta]): The expiration time for the token.

    Returns:
        str: The generated JWT token.

    Example:
        data = {'sub': 'user_id'}
        create_access_token(data)
        > 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def login_user(username: str, password: str) -> LoginResponseModel:
    """
    Authenticates a user. Expects a username and password, returns a JWT token upon successful authentication.

    Args:
        username (str): The username of the user attempting to log in.
        password (str): The password of the user attempting to log in.

    Returns:
        LoginResponseModel: This model returns the JWT token upon successful authentication.

    Example:
        username = 'john.doe'
        password = 'securepassword'
        login_user(username, password)
        > LoginResponseModel(token='eyJ0eXAiOiJ...')
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": username})
    if not user:
        raise ValueError("Invalid username or password")
    if not await verify_password(password, user.password):
        raise ValueError("Invalid username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return LoginResponseModel(token=access_token)
