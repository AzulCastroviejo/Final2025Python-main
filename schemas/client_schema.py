"""Client schema for request/response validation."""
from typing import Optional
from pydantic import EmailStr, Field, field_validator
from models.enums import UserRole

from schemas.base_schema import BaseSchema

# Main schema for reading/responding client data (password is not sent)
class ClientSchema(BaseSchema):
    """Schema for Client entity validation. Used for reading/returning client data."""

    name: str = Field(..., min_length=1, max_length=100, description="Client's first name")
    lastname: str = Field(..., min_length=1, max_length=100, description="Client's last name")
    email: EmailStr = Field(..., description="Client's email address")
    telephone: Optional[str] = Field(
        None,
        min_length=7,
        max_length=20,
        pattern=r'^\+?[1-9]\d{6,19}$',
        description="Client's phone number (7-20 digits, optional + prefix)"
    )
    role: UserRole  
    # Password is made optional and excluded from the response by default.
    password: Optional[str] = Field(default=None, exclude=True)

    @field_validator('telephone', mode='before')
    @classmethod
    def empty_str_to_none(cls, v):
        """Convert empty string to None for optional telephone field."""
        if isinstance(v, str) and v == '':
            return None
        return v

# Schema specifically for creating a new client (password is required)
class ClientCreateSchema(ClientSchema):
    """Schema for creating a new client. Requires password."""
    password: str = Field(..., min_length=8, description="User password (at least 8 characters)")
