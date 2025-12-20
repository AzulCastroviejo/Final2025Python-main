# schemas/order_schema.py - VERSIÓN CORREGIDA
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class OrderItemSchema(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    price: float = Field(gt=0)

class OrderSchema(BaseModel):
    # Datos del cliente (como los envías desde el frontend)
    client_name: str
    client_email: str
    client_phone: str
    shipping_address: str
    payment_method: str
    
    # Campos que ahora son OPCIONALES
    delivery_method: Optional[int] = Field(default=3, description="1=DRIVE_THRU, 2=ON_HAND, 3=HOME_DELIVERY")
    client_id: Optional[int] = None
    bill_id: Optional[int] = None
    
    # Items de la orden
    items: List[OrderItemSchema]
    
    # Totales
    subtotal: float = Field(ge=0)
    tax: float = Field(ge=0)
    shipping_cost: float = Field(ge=0)
    total: float = Field(ge=0)
    status: str = Field(default="pending")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "client_name": "Juan Pérez",
                "client_email": "juan@example.com",
                "client_phone": "2612077095",
                "shipping_address": "Calle Falsa 123",
                "payment_method": "card",
                "delivery_method": 3,
                "client_id": 1,
                "bill_id": 1,
                "items": [
                    {
                        "product_id": 1,
                        "quantity": 2,
                        "price": 1500000
                    }
                ],
                "subtotal": 3000000,
                "tax": 480000,
                "shipping_cost": 0,
                "total": 3480000,
                "status": "pending"
            }
        }

class OrderResponseSchema(BaseModel):
    id_key: int
    client_name: str
    client_email: str
    client_phone: str
    shipping_address: str
    payment_method: str
    delivery_method: Optional[int]
    client_id: Optional[int]
    bill_id: Optional[int]
    subtotal: float
    tax: float
    shipping_cost: float
    total: float
    status: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True