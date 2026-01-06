"""
Client controller with a protected /me endpoint and corrected routing order.
This controller takes full control of its route registration to solve ordering
issues with the generic BaseControllerImpl.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.client import ClientModel
from schemas.client_schema import ClientSchema, ClientCreateSchema
from services.auth_service import get_current_user
from services.client_service import ClientService
from config.database import get_db
from controllers.base_controller_impl import BaseControllerImpl

class ClientController:
    """
    Controller for Client entity.

    This implementation manually defines all routes to ensure the specific
    `/me` route is registered before the generic `/{id_key}` route, solving
    the routing conflict. It also properly overrides the create method to handle
    duplicate user registration gracefully.
    """

    def __init__(self):
        """Initializes the controller and sets up the router with the correct route order."""
        self.router = APIRouter(tags=["Clients"])
        self.service_factory = lambda db: ClientService(db)
        self.schema = ClientSchema

        # 1. Register the most specific route FIRST to avoid conflicts.
        self.router.add_api_route("/me", self.get_me, methods=["GET"], response_model=self.schema)

        # 2. Register the standard CRUD routes.
        self.router.add_api_route("/", self.get_all, methods=["GET"], response_model=list[self.schema])
        self.router.add_api_route("/{id_key}", self.get_one, methods=["GET"], response_model=self.schema)
        
        # Point the POST route to our custom `create` method with error handling.
        self.router.add_api_route("/", self.create, methods=["POST"], status_code=201, response_model=self.schema)
        
        self.router.add_api_route("/{id_key}", self.update, methods=["PUT"], response_model=self.schema)
        self.router.add_api_route("/{id_key}", self.delete, methods=["DELETE"], status_code=204)

    async def get_me(self, current_user: ClientModel = Depends(get_current_user)):
        """Returns the profile of the currently authenticated user."""
        return current_user

    def create(self, schema_in: ClientCreateSchema, db: Session = Depends(get_db)):
        """
        Handles the creation of a new client, with specific error handling for duplicates.
        """
        service = self.service_factory(db)
        try:
            return service.save(schema_in)
        except ValueError as e:
            # If the user already exists, return a 409 Conflict.
            detail_message = {
                "msg": f"El correo electrónico '{schema_in.email}' ya está registrado.",
                "suggestion": "Por favor, intenta iniciar sesión.",
                "login_url": "/token"
            }
            raise HTTPException(status_code=409, detail=detail_message)

    # The following methods replicate the behavior of BaseControllerImpl
    def get_all(self, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        service = self.service_factory(db)
        return service.get_all(skip=skip, limit=limit)

    def get_one(self, id_key: int, db: Session = Depends(get_db)):
        service = self.service_factory(db)
        return service.get_one(id_key)

    def update(self, id_key: int, schema_in: ClientSchema, db: Session = Depends(get_db)):
        service = self.service_factory(db)
        return service.update(id_key, schema_in)

    def delete(self, id_key: int, db: Session = Depends(get_db)):
        service = self.service_factory(db)
        service.delete(id_key)
        return None
