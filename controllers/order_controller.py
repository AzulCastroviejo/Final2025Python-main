"""Order controller with authentication for creation."""
from fastapi import Depends, status
from sqlalchemy.orm import Session

from config.database import get_db
from controllers.base_controller_impl import BaseControllerImpl
from models.client import ClientModel
from schemas.order_schema import OrderSchema
from services.auth_service import get_current_user
from services.order_service import OrderService


class OrderController(BaseControllerImpl):
    """Controller for Order entity, with protected creation endpoint."""

    def __init__(self):
        """
        Initializes the controller, calling the base constructor and then
        overriding the POST endpoint to add authentication.
        """
        super().__init__(
            schema=OrderSchema,
            service_factory=lambda db: OrderService(db),
            tags=["Orders"]
        )

        # Remove the automatically generated POST route
        self.router.routes = [route for route in self.router.routes if route.path != "/" or "POST" not in route.methods]

        # Add the new protected POST route
        self._add_protected_create_route()

    def _add_protected_create_route(self):
        """
        Adds a new POST endpoint for creating an order, requiring user authentication.
        The order is automatically associated with the authenticated user.
        """
        @self.router.post("/", response_model=self.schema, status_code=status.HTTP_201_CREATED)
        def create_order_for_current_user(
            order_data: self.schema,
            db: Session = Depends(get_db),
            current_user: ClientModel = Depends(get_current_user)
        ):
            """
            Create a new order for the currently authenticated user.
            The `client_id_key` in the request body will be ignored; the authenticated
            user's ID will be used instead.
            """
            service = self.service_factory(db)
            
            # Associate the order with the logged-in user
            order_data.client_id_key = current_user.id_key

            # Save the order
            return service.save(order_data)
