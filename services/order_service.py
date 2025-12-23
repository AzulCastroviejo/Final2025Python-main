"""OrderService with foreign key validation, business logic, and email notifications."""
from typing import List
from sqlalchemy.orm import Session, joinedload, selectinload
from datetime import datetime

from models.order import OrderModel
from models.order_detail import OrderDetailModel
from models.client import ClientModel
from repositories.order_repository import OrderRepository
from repositories.client_repository import ClientRepository
from repositories.bill_repository import BillRepository
from repositories.base_repository_impl import InstanceNotFoundError
from schemas.order_schema import OrderSchema
from services.base_service_impl import BaseServiceImpl
from utils.logging_utils import get_sanitized_logger
#from utils.email_utils import send_order_confirmation_email

logger = get_sanitized_logger(__name__)


class OrderService(BaseServiceImpl):
    """Service for Order entity with validation, business logic, and notifications."""

    def __init__(self, db: Session):
        super().__init__(
            repository_class=OrderRepository,
            model=OrderModel,
            schema=OrderSchema,
            db=db
        )
        self._client_repository = ClientRepository(db)
        self._bill_repository = BillRepository(db)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[OrderSchema]:
        """
        Get all orders with pagination, including related client and order details.

        This method overrides the base implementation to eagerly load relationships
        for efficient data retrieval.

        Args:
            skip: Number of records to skip for pagination.
            limit: Maximum number of records to return.

        Returns:
            A list of order schemas with nested details.
        """
        logger.info(f"Fetching orders (skip={skip}, limit={limit}) with client and product details")

        # Eagerly load relationships to avoid N+1 query problems.
        # - `joinedload` for many-to-one (order -> client)
        # - `selectinload` for one-to-many (order -> order_details -> product)
        load_options = [
            joinedload(OrderModel.client),
            selectinload(OrderModel.order_details).joinedload(OrderDetailModel.product)
        ]
        
        models = self._repository.find_all(skip=skip, limit=limit, load_options=load_options)
        
        # Convert ORM models to Pydantic schemas
        return [self._schema.model_validate(model) for model in models]

    def get_one(self, id_key: int) -> OrderSchema:
        """
        Get a single order by its ID, including related client, order details, and products.

        Args:
            id_key: The ID of the order.

        Returns:
            The order schema with nested details.
        """
        logger.info(f"Fetching order {id_key} with details, products, and client via eager loading")

        # Eagerly load the client and the order_details with their respective products.
        load_options = [
            joinedload(OrderModel.client),
            selectinload(OrderModel.order_details).joinedload(OrderDetailModel.product)
        ]

        model = self._repository.find(id_key, load_options=load_options)

        return self._schema.model_validate(model)

    def save(self, schema: OrderSchema) -> OrderSchema:
        """
        Create a new order, validate foreign keys, and send a confirmation email.

        Args:
            schema: Order data to create.

        Returns:
            The created order schema.
        """
        # 1. Validate foreign keys
        try:
            self._client_repository.find(schema.client_id)
            self._bill_repository.find(schema.bill_id)
        except InstanceNotFoundError as e:
            logger.error(f"Validation failed for new order: {e}")
            raise

        # 2. Set creation date and create the order
        if schema.date is None:
            schema.date = datetime.utcnow()
        
        logger.info(f"Creating order for client {schema.client_id}")
        created_order_schema = super().save(schema)
        logger.info(f"Successfully created order {created_order_schema.id_key}")

        # 3. Send confirmation email (in a try-except block to not fail the transaction)
        try:
            logger.info(f"Preparing to send confirmation email for order {created_order_schema.id_key}")
            full_order_data = self.get_one(created_order_schema.id_key)

            if full_order_data.client and full_order_data.client.email:
                order_details_dict = [
                    detail.model_dump() for detail in full_order_data.order_details
                ]
                
                send_order_confirmation_email(
                    client_email=full_order_data.client.email,
                    client_name=full_order_data.client.name or "Cliente",
                    order_id=full_order_data.id_key,
                    total=full_order_data.total,
                    order_details=order_details_dict
                )
            else:
                logger.warning(f"Cannot send email for order {created_order_schema.id_key}: Client data or email is missing.")

        except Exception as e:
            logger.error(
                f"Order {created_order_schema.id_key} was created, but failed to send confirmation email. Error: {e}",
                exc_info=True
            )

        return created_order_schema

    def update(self, id_key: int, schema: OrderSchema) -> OrderSchema:
        """
        Update an order with validation.
        """
        if schema.client_id is not None:
            try:
                self._client_repository.find(schema.client_id)
            except InstanceNotFoundError:
                logger.error(f"Client with id {schema.client_id} not found")
                raise

        if schema.bill_id is not None:
            try:
                self._bill_repository.find(schema.bill_id)
            except InstanceNotFoundError:
                logger.error(f"Bill with id {schema.bill_id} not found")
                raise

        logger.info(f"Updating order {id_key}")
        return super().update(id_key, schema)
