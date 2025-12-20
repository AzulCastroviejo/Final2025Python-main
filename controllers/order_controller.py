# controllers/order_controller.py - VERSIÓN CON CLASE
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from schemas.order_schema import OrderSchema, OrderResponseSchema
from services.order_service import OrderService
from controllers.base_controller_impl import BaseControllerImpl
import logging

logger = logging.getLogger(__name__)


class OrderController(BaseControllerImpl):
    """Controller para gestionar órdenes"""
    
    def __init__(self):
        # Inicializar el router
        self.router = APIRouter(prefix="/orders", tags=["Orders"])
        
        # Registrar las rutas
        self._register_routes()
    
    def _register_routes(self):
        """Registrar todas las rutas del controller"""
        
        @self.router.post("/", response_model=OrderResponseSchema, status_code=status.HTTP_201_CREATED)
        def create_order(
            order: OrderSchema,
            db: Session = Depends(get_db)
        ):
            """
            Crear una nueva orden.
            
            Esta versión crea automáticamente:
            - El cliente (si no existe)
            - La factura
            - La orden con todos sus items
            
            Campos requeridos:
            - client_name, client_email, client_phone
            - shipping_address, payment_method
            - items (lista de productos)
            - subtotal, tax, shipping_cost, total
            
            Campos opcionales:
            - delivery_method (default: 3 = HOME_DELIVERY)
            - client_id (se crea si no se proporciona)
            - bill_id (se crea si no se proporciona)
            """
            try:
                service = OrderService(db)
                new_order = service.create_order_with_client_and_bill(order)
                logger.info(f"Orden {new_order.id_key} creada exitosamente")
                return new_order
            except Exception as e:
                logger.error(f"Error al crear orden: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Error al crear la orden: {str(e)}"
                )
        
        @self.router.get("/", response_model=List[OrderResponseSchema])
        def get_orders(
            skip: int = 0,
            limit: int = 100,
            db: Session = Depends(get_db)
        ):
            """Obtener todas las órdenes con paginación"""
            try:
                service = OrderService(db)
                orders = service.get_all_orders(skip=skip, limit=limit)
                return orders
            except Exception as e:
                logger.error(f"Error al obtener órdenes: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error al obtener órdenes: {str(e)}"
                )
        
        @self.router.get("/{order_id}", response_model=OrderResponseSchema)
        def get_order(
            order_id: int,
            db: Session = Depends(get_db)
        ):
            """Obtener una orden por ID"""
            try:
                service = OrderService(db)
                order = service.get_order_by_id(order_id)
                if not order:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Orden con ID {order_id} no encontrada"
                    )
                return order
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Error al obtener orden {order_id}: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error al obtener orden: {str(e)}"
                )
        
        @self.router.put("/{order_id}", response_model=OrderResponseSchema)
        def update_order(
            order_id: int,
            order: OrderSchema,
            db: Session = Depends(get_db)
        ):
            """Actualizar una orden existente"""
            try:
                service = OrderService(db)
                updated_order = service.update_order(order_id, order)
                if not updated_order:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Orden con ID {order_id} no encontrada"
                    )
                return updated_order
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Error al actualizar orden {order_id}: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Error al actualizar orden: {str(e)}"
                )
        
        @self.router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
        def delete_order(
            order_id: int,
            db: Session = Depends(get_db)
        ):
            """Eliminar una orden"""
            try:
                service = OrderService(db)
                deleted = service.delete_order(order_id)
                if not deleted:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Orden con ID {order_id} no encontrada"
                    )
                return None
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Error al eliminar orden {order_id}: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Error al eliminar orden: {str(e)}"
                )
    
    def get_router(self):
        """Retornar el router para incluirlo en la app"""
        return self.router
