"""Schema for JWT token responses."""
from typing import Optional
from pydantic import BaseModel


class TokenSchema(BaseModel):
    """Defines the structure for the access token response."""
    access_token: str
    token_type: str


class TokenDataSchema(BaseModel):
    """Defines the data encoded within the JWT token."""
    email: Optional[str] = None
    role: Optional[str] = None
