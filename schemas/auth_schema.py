"""
Authentication Schemas Module

This module defines the Pydantic schemas for authentication-related data,
including tokens, user registration, and login.
"""

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    """Schema for the access token response."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for the data encoded within the JWT token."""
    email: EmailStr | None = None


class UserCreate(BaseModel):
    """Schema for user registration request."""
    email: EmailStr
    password: str
    name: str
    lastname: str


class UserLogin(BaseModel):
    """Schema for user login request."""
    email: EmailStr
    password: str


class UserInDB(UserCreate):
    """Schema to represent a user as stored in the database."""
    hashed_password: str
