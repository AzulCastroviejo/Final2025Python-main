"""Controller for handling user authentication and token generation."""
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from schemas.token_schema import TokenSchema
from services.auth_service import AuthService


class AuthController:
    """
    Exposes the /token endpoint for user authentication.
    """

    def __init__(self):
        """Initializes the router and defines the authentication route."""
        self.router = APIRouter(
            tags=["Authentication"],
            prefix="/auth"
        )
        self._register_routes()

    def _register_routes(self):
        """
        Registers the login endpoint.
        """
        @self.router.post("/token", response_model=TokenSchema)
        async def login_for_access_token(
            form_data: OAuth2PasswordRequestForm = Depends(),
            auth_service: AuthService = Depends(AuthService)
        ):
            """
            Handles the POST request to /token to authenticate a user.

            It uses FastAPI's `OAuth2PasswordRequestForm` which expects a form-data
            body with `username` and `password` fields.

            Args:
                form_data: The user's credentials (username and password).
                auth_service: The authentication service, injected as a dependency.

            Returns:
                An access token and token type.
            """
            return auth_service.login_for_access_token(form_data)

# Single instance of the controller to be used in the main application
auth_controller = AuthController()
