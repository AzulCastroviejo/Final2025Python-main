"""Client service for handling business logic related to clients."""
from sqlalchemy.orm import Session
from models.client import ClientModel
from repositories.client_repository import ClientRepository
from schemas.client_schema import ClientSchema
from services.base_service_impl import BaseServiceImpl
from utils.logging_utils import get_sanitized_logger
from utils.security import get_password_hash

logger = get_sanitized_logger(__name__)

class ClientService(BaseServiceImpl):
    """
    Service for Client entity, handles password hashing for new users.
    """
    def __init__(self, db: Session):
        super().__init__(
            repository_class=ClientRepository,
            model=ClientModel,
            schema=ClientSchema,
            db=db
        )

    def save(self, schema: ClientSchema) -> ClientSchema:
        """
        Creates a new client after validating and hashing the password.

        If a client with the same email already exists, it raises an error.

        Args:
            schema: The client registration data, including a plain-text password.

        Returns:
            The newly created client schema (without the password).

        Raises:
            ValueError: If the email already exists or if the password is not provided.
        """
        if not schema.email:
            logger.error("Email is required to create a client.")
            raise ValueError("Email is required to create a client.")

        repo: ClientRepository = self._repository
        existing_client = repo.find_by_email(schema.email)

        if existing_client:
            logger.warning(f"Registration attempt for existing email: {schema.email}")
            raise ValueError(f"A client with email {schema.email} already exists.")
        
        if not schema.password:
            logger.error("Password is required for new client registration.")
            raise ValueError("Password is required for new client registration.")

        logger.info(f"Creating a new client with email: {schema.email}")

        # Convert schema to dict, excluding the password field which is write-only
        client_data = schema.model_dump(exclude={"password"})

        # Hash the password and create the model instance
        hashed_password = get_password_hash(schema.password)
        new_client_model = self._model(**client_data, hashed_password=hashed_password)

        # Save the new model using the repository
        saved_model = repo.save(new_client_model)
        
        # Convert the saved model back to a schema for the response
        return self.to_schema(saved_model)
