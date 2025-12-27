"""Service for handling user authentication, token generation, and authorization."""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from models.client import ClientModel
from models.enums import UserRole
from repositories.client_repository import ClientRepository
from schemas.token_schema import TokenSchema, TokenDataSchema
from utils.security import create_access_token, verify_password, decode_access_token
from config.database import get_db

# This tells FastAPI where to go to get the token. 
# It points to the 'login_for_access_token' function in AuthController.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


class AuthService:
    """
    Provides authentication services, including user verification and token creation.
    """

    def __init__(self, db: Session = Depends(get_db)):
        """
        Initializes the service with a database session.
        Args:
            db: The SQLAlchemy session, injected by FastAPI.
        """
        self.client_repository = ClientRepository(db)
        self.db = db

    def login_for_access_token(self, form_data: OAuth2PasswordRequestForm) -> TokenSchema:
        """
        Authenticates a user and returns a JWT access token.
        Args:
            form_data: The username (email) and password from the client.
        Returns:
            A TokenSchema containing the access token and token type.
        Raises:
            HTTPException: If authentication fails.
        """
        client = self.client_repository.find_by_email(form_data.username)

        if not client or not verify_password(form_data.password, client.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(
            data={"sub": client.email, "role": client.role.value}
        )

        return TokenSchema(access_token=access_token, token_type="bearer")

# --- Authorization Dependencies ---

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> ClientModel:
    """
    Dependency to get the current user from a JWT token.
    Verifies token, decodes it, and fetches the user from the database.
    Args:
        token: The OAuth2 token.
        db: The database session.
    Returns:
        The authenticated user model.
    Raises:
        HTTPException: If the token is invalid or the user is not found.
    """
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception

    client_repository = ClientRepository(db)
    user = client_repository.find_by_email(email)
    
    if user is None:
        raise credentials_exception
        
    return user

async def get_current_admin_user(current_user: ClientModel = Depends(get_current_user)) -> ClientModel:
    """
    Dependency to get the current admin user. 
    Ensures the user is authenticated and has the ADMIN role.
    Args:
        current_user: The user model from `get_current_user`.
    Returns:
        The authenticated admin user model.
    Raises:
        HTTPException: If the user is not an admin.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user does not have enough privileges",
        )
    return current_user
