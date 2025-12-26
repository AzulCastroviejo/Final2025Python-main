"""
Authentication Service Module

This module contains the core business logic for handling security,
including password hashing, JWT token creation and verification,
and user retrieval from the database.
"""

from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from models.client import ClientModel

# --- Security Configuration ---

# This should be a strong, randomly generated secret key and stored securely
# in an environment variable, NOT hardcoded.
# Example for generation: openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # The token will be valid for 30 minutes

# Configure password hashing using bcrypt algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# --- Password Management ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies that a plain text password matches a hashed password.

    Args:
        plain_password: The password provided by the user during login.
        hashed_password: The hashed password stored in the database.

    Returns:
        True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hashes a plain text password using bcrypt.

    Args:
        password: The plain text password from user registration.

    Returns:
        The hashed password to be stored in the database.
    """
    return pwd_context.hash(password)


# --- JWT Token Management ---

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a new JWT access token.

    Args:
        data: A dictionary containing the claims to include in the token (e.g., user email, role).
        expires_delta: An optional timedelta to specify a custom token lifetime.

    Returns:
        The encoded JWT token as a string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# --- Database Operations ---

def get_user(db: Session, email: str) -> Optional[ClientModel]:
    """
    Retrieves a user from the database by their email address.

    Args:
        db: The SQLAlchemy database session.
        email: The email of the user to find.

    Returns:
        The ClientModel instance if found, otherwise None.
    """
    return db.query(ClientModel).filter(ClientModel.email == email).first()
