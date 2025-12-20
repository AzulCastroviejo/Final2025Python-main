# schemas/order_schema.py - VERSIÓN FINAL CORREGIDA
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class OrderItemSchema(BaseModel):
    """Schema para items individuales de la orden"""
    product_id: int = Field(..., description="ID del producto")
    quantity: int = Field(..., gt=0, description="Cantidad del producto")
    price: float = Field(..., gt=0, description="Precio unitario del producto")
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "product_id": 1,
                "quantity": 2,
                "price": 1500000
            }
        }
    }


class OrderSchema(BaseModel):
    """Schema para crear/actualizar órdenes"""
    # Datos del cliente (como los envías desde el frontend)
    client_name: str = Field(..., min_length=1, description="Nombre completo del cliente")
    client_email: str = Field(..., description="Email del cliente")
    client_phone: str = Field(..., description="Teléfono del cliente")
    shipping_address: str = Field(..., min_length=1, description="Dirección de envío")
    payment_method: str = Field(..., description="Método de pago: card o cash")
    
    # Campos que ahora son OPCIONALES
    delivery_method: Optional[int] = Field(
        default=3, 
        ge=1, 
        le=3,
        description="Método de entrega: 1=DRIVE_THRU, 2=ON_HAND, 3=HOME_DELIVERY"
    )
    client_id: Optional[int] = Field(default=None, description="ID del cliente (se crea si no existe)")
    bill_id: Optional[int] = Field(default=None, description="ID de la factura (se crea si no existe)")
    
    # Items de la orden
    items: List[OrderItemSchema] = Field(..., min_length=1, description="Lista de productos en la orden")
    
    # Totales
    subtotal: float = Field(..., ge=0, description="Subtotal de la orden")
    tax: float = Field(..., ge=0, description="Impuestos")
    shipping_cost: float = Field(..., ge=0, description="Costo de envío")
    total: float = Field(..., ge=0, description="Total de la orden")
    status: str = Field(default="pending", description="Estado de la orden")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
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
    }


class OrderResponseSchema(BaseModel):
    """Schema para respuestas de órdenes"""
    id_key: int
    client_name: str
    client_email: str
    client_phone: str
    shipping_address: str
    payment_method: str
    delivery_method: Optional[int] = None
    client_id: Optional[int] = None
    bill_id: Optional[int] = None
    subtotal: float
    tax: float
    shipping_cost: float
    total: float
    status: str
    created_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }
