"""Client controller with protected /me endpoint and cleaned up routes."""
from fastapi import Depends

from controllers.base_controller_impl import BaseControllerImpl
from models.client import ClientModel
from schemas.client_schema import ClientSchema
from services.auth_service import get_current_user
from services.client_service import ClientService


class ClientController(BaseControllerImpl):
    """Controller for Client entity with a protected /me endpoint."""

    def __init__(self):
        """
        Initializes the controller, adds the /me route, and removes the now-obsolete
        and insecure client_login functionality.
        """
        super().__init__(
            schema=ClientSchema,
            service_factory=lambda db: ClientService(db),
            tags=["Clients"]
        )

        self._add_me_route()

    def _add_me_route(self):
        """
        Adds the `GET /me` endpoint to retrieve the current user's profile.
        """
        @self.router.get("/me", response_model=self.schema)
        async def get_me(current_user: ClientModel = Depends(get_current_user)):
            """
            Returns the profile of the currently authenticated user.
            The user is identified via the JWT token in the Authorization header.
            """
            return current_user
