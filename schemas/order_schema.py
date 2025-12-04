"""Order schema with validation."""
from datetime import datetime
from typing import Optional
from pydantic import Field

from schemas.base_schema import BaseSchema
from models.enums import DeliveryMethod, Status


class OrderSchema(BaseSchema):
    """Schema for Order entity with validations."""

    date: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Order date")
    total: float = Field(..., ge=0, description="Total amount (must be >= 0, required)")
    delivery_method: int = Field(
        ...,
        ge=1,
        le=3,
        description="Delivery method (1=Drive-thru, 2=On-hand, 3=Home)",
        # json_schema_extra={"enum": [1, 2, 3]} # Opcional: para docs
    )
    status: int = Field(
        ..., ge=1, le=3,
        description="Order status (1=Pending, 2=Completed, 3=Cancelled)"
    )
    client_id: int = Field(..., description="Client ID reference (required)")
    bill_id: int = Field(..., description="Bill ID reference (required)")

