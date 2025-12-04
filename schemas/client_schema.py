"""Client schema for request/response validation."""
from typing import Optional, List, TYPE_CHECKING
from pydantic import EmailStr, Field
from schemas.address_schema import AddressSchema
from schemas.base_schema import BaseSchema
from schemas.order_schema import OrderSchema

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
    # 1. Definir las relaciones con 'Optional' y 'List'
    orders: Optional[List[OrderSchema]] = None
    addresses: Optional[List[AddressSchema]] = None

    # 2. Corregir la Serialización de Lectura
    model_config = {
        "from_attributes": True, # Necesario para Pydantic 2.x
        # Excluir las relaciones para evitar bucles cuando el esquema es usado internamente (ej., en OrderService)
        "exclude": ["orders", "addresses"]
    }
   # addresses: Optional[List['AddressSchema']] = []
    #orders: Optional[List['OrderSchema']] = []
