"""Client schema for request/response validation."""
from typing import Optional, List, TYPE_CHECKING
from pydantic import EmailStr, Field

from schemas.base_schema import BaseSchema

if TYPE_CHECKING:
    from schemas.address_schema import AddressSchema
    from schemas.order_schema import OrderSchema


class ClientSchema(BaseSchema):
    """Schema for Client entity with validations."""

    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Client's first name")
    lastname: Optional[str] = Field(None, min_length=1, max_length=100, description="Client's last name")
    email: Optional[EmailStr] = Field(None, description="Client's email address")
    telephone: Optional[str] = Field(
        None,
        min_length=7,
        max_length=20,
        pattern=r'^\+?[1-9]\d{6,19}$',
        description="Client's phone number (7-20 digits, optional + prefix)"
    )
    addresses: Optional[List['AddressSchema']] = []
    orders: Optional[List['OrderSchema']] = []


# --- Runtime Resolution for Forward References ---
# This is the crucial part that solves the PydanticUndefinedAnnotation error.
# We import the schemas here, outside the TYPE_CHECKING block, so they are
# available at runtime. Then, we explicitly tell ClientSchema how to resolve
# the string-based forward references ('AddressSchema', 'OrderSchema').

from schemas.address_schema import AddressSchema
from schemas.order_schema import OrderSchema

ClientSchema.update_forward_refs(AddressSchema=AddressSchema, OrderSchema=OrderSchema)
