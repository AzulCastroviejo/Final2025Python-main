# services/order_service.py - VERSIÓN CORREGIDA PARA TU MODELO
from sqlalchemy.orm import Session
from models.order import OrderModel
from models.client import ClientModel
from models.bill import BillModel
from models.order_detail import OrderDetailModel
from schemas.order_schema import OrderSchema
from repositories.client_repository import ClientRepository
from repositories.bill_repository import BillRepository
from repositories.order_repository import OrderRepository
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)


class OrderService:
    """Servicio para gestionar órdenes con creación automática de cliente y factura"""
    
    def __init__(self, db: Session):
        self.db = db
        self.order_repository = OrderRepository(db)
        self.client_repository = ClientRepository(db)
        self.bill_repository = BillRepository(db)

    def create_order_with_client_and_bill(self, order_data: OrderSchema):
        """
        Crea una orden completa:
        1. Busca o crea el cliente
        2. Crea la factura
        3. Crea la orden con todos los campos requeridos
        4. Crea los order_details
        """
        try:
            # PASO 1: Buscar o crear el cliente
            client_id = order_data.client_id
            
            if not client_id:
                # Buscar cliente existente por email
                existing_client = self.db.query(ClientModel).filter(
                    ClientModel.email == order_data.client_email
                ).first()
                
                if existing_client:
                    client_id = existing_client.id_key
                    logger.info(f"Cliente existente encontrado: {client_id}")
                else:
                    # Crear nuevo cliente
                    # Dividir el nombre completo
                    name_parts = order_data.client_name.strip().split(' ', 1)
                    first_name = name_parts[0]
                    last_name = name_parts[1] if len(name_parts) > 1 else first_name
                    
                    new_client = ClientModel(
                        name=first_name,
                        lastname=last_name,
                        email=order_data.client_email,
                        telephone=order_data.client_phone
                    )
                    self.db.add(new_client)
                    self.db.flush()  # Para obtener el ID sin hacer commit
                    client_id = new_client.id_key
                    logger.info(f"Nuevo cliente creado: {client_id}")

            # PASO 2: Crear la factura (bill)
            bill_id = order_data.bill_id
            
            if not bill_id:
                # Generar número de factura único
                bill_number = f"BILL-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                
                new_bill = BillModel(
                    bill_number=bill_number,
                    discount=0,
                    date=date.today(),
                    total=order_data.total,
                    payment_type=order_data.payment_method
                )
                self.db.add(new_bill)
                self.db.flush()  # Para obtener el ID sin hacer commit
                bill_id = new_bill.id_key
                logger.info(f"Nueva factura creada: {bill_id} ({bill_number})")

            # PASO 3: Mapear delivery_method de número a string
            delivery_method_map = {
                1: "drive_thru",
                2: "on_hand",
                3: "home_delivery"
            }
            delivery_method_str = delivery_method_map.get(
                order_data.delivery_method, 
                "home_delivery"  # default
            )

            # PASO 4: Crear la orden (SOLO con los campos que existen en tu modelo)
            new_order = OrderModel(
                date=datetime.now(),
                total=order_data.total,
                delivery_method=delivery_method_str,  # String, no Integer
                status=1,  # PENDING (si Status es Enum con valor 1)
                client_id=client_id,
                bill_id=bill_id
            )
            
            self.db.add(new_order)
            self.db.flush()
            
            # PASO 5: Crear los items de la orden (order_details)
            for item in order_data.items:
                order_detail = OrderDetailModel(
                    quantity=item.quantity,
                    price=item.price,
                    order_id=new_order.id_key,
                    product_id=item.product_id
                )
                self.db.add(order_detail)
            
            # Hacer commit de todo junto (transacción completa)
            self.db.commit()
            self.db.refresh(new_order)
            
            logger.info(f"✅ Orden creada exitosamente: {new_order.id_key}")
            return new_order

        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error creando orden: {str(e)}")
            raise e

    def get_all_orders(self, skip: int = 0, limit: int = 100):
        """Obtener todas las órdenes con paginación"""
        try:
            return self.order_repository.find_all(skip=skip, limit=limit)
        except Exception as e:
            logger.error(f"Error obteniendo órdenes: {str(e)}")
            raise e

    def get_order_by_id(self, order_id: int):
        """Obtener orden por ID"""
        try:
            return self.order_repository.find(order_id)
        except Exception as e:
            logger.error(f"Error obteniendo orden {order_id}: {str(e)}")
            raise e

    def update_order(self, order_id: int, order_data: OrderSchema):
        """Actualizar una orden"""
        try:
            return self.order_repository.update(
                order_id, 
                order_data.model_dump(exclude_unset=True)
            )
        except Exception as e:
            logger.error(f"Error actualizando orden {order_id}: {str(e)}")
            raise e

    def delete_order(self, order_id: int):
        """Eliminar una orden"""
        try:
            return self.order_repository.remove(order_id)
        except Exception as e:
            logger.error(f"Error eliminando orden {order_id}: {str(e)}")
            raise e
