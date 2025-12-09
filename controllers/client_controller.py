"""Client controller with proper dependency injection."""

from fastapi import APIRouter, Depends
from controllers.base_controller_impl import BaseControllerImpl
from schemas.client_schema import ClientSchema
from services.client_service import ClientService
from sqlalchemy.orm import Session
from config.database import get_db

class ClientController(BaseControllerImpl):
    """Controller for Client entity with CRUD operations."""

    def __init__(self):
        """
        Initialize ClientController with dependency injection.

        The service is created per request with the database session.
        """
        super().__init__(
            schema=ClientSchema,
            service_factory=lambda db: ClientService(db),
            tags=["Clients"]
        )

    @self.router.get("/login")
    def login(email: str, password: str, db: Session = Depends(get_db)):
        service = ClientService(db)
        user = service.login(email, password)
        return user