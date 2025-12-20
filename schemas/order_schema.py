# schemas/order_schema.py - VERSIÓN FINAL AJUSTADA A TU MODELO
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Union
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
    # delivery_method acepta int (1,2,3) o string ("drive_thru", "on_hand", "home_delivery")
    delivery_method: Optional[Union[int, str]] = Field(
        default=3, 
        description="Método de entrega: 1=drive_thru, 2=on_hand, 3=home_delivery"
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

    @field_validator('delivery_method')
    @classmethod
    def validate_delivery_method(cls, v):
        """Validar que delivery_method sea válido"""
        valid_ints = [1, 2, 3]
        valid_strings = ["drive_thru", "on_hand", "home_delivery"]
        
        if isinstance(v, int) and v not in valid_ints:
            raise ValueError(f"delivery_method debe ser 1, 2 o 3. Recibido: {v}")
        elif isinstance(v, str) and v not in valid_strings:
            raise ValueError(f"delivery_method debe ser 'drive_thru', 'on_hand' o 'home_delivery'. Recibido: {v}")
        
        return v

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
    date: Optional[datetime] = None
    total: float
    delivery_method: Optional[str] = None
    status: Optional[int] = None
    client_id: Optional[int] = None
    bill_id: Optional[int] = None

    model_config = {
        "from_attributes": True
    }
