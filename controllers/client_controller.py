"""Client controller with protected /me endpoint and cleaned up routes."""
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from controllers.base_controller_impl import BaseControllerImpl
from models.client import ClientModel
# Import the new create schema
from schemas.client_schema import ClientSchema, ClientCreateSchema
from services.auth_service import get_current_user
from services.client_service import ClientService
from config.database import get_db

class ClientController(BaseControllerImpl):
    """Controller for Client entity with a protected /me endpoint."""

    def __init__(self):
        """
        Initializes the controller, adds the /me route, and removes the now-obsolete
        and insecure client_login functionality.
        """
        super().__init__(
            # The main schema is the read-schema (ClientSchema)
            schema=ClientSchema,
            service_factory=lambda db: ClientService(db),
            tags=["Clients"]
        )

        self._add_me_route()
        self._add_create_route()

    def _add_me_route(self):
        """
        Adds the `GET /me` endpoint to retrieve the current user's profile.
        """
        # Response model is the read schema
        @self.router.get("/me", response_model=self.schema)
        async def get_me(current_user: ClientModel = Depends(get_current_user)):
            """
            Returns the profile of the currently authenticated user.
            The user is identified via the JWT token in the Authorization header.
            """
            return current_user
    
    def _add_create_route(self):
        # Response model is the read schema, but the input uses the create schema
        @self.router.post("/", response_model=self.schema, status_code=201)
        def create(schema_in: ClientCreateSchema, db: Session = Depends(get_db)):
            service = self.service_factory(db)
            try:
                # Pass the create schema to the service
                return service.save(schema_in)
            except ValueError as e:
                raise HTTPException(status_code=409, detail=str(e))
