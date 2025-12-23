from sqlalchemy.orm import Session
from models.client import ClientModel
from repositories.client_repository import ClientRepository
from schemas.client_schema import ClientSchema
from services.base_service_impl import BaseServiceImpl
from utils.logging_utils import get_sanitized_logger

logger = get_sanitized_logger(__name__)


class ClientService(BaseServiceImpl):
    def __init__(self, db: Session):
        super().__init__(
            repository_class=ClientRepository,
            model=ClientModel,
            schema=ClientSchema,
            db=db
        )

    def save(self, schema: ClientSchema) -> ClientSchema:
        """
        Gets or creates a client.

        If a client with the same email already exists, it returns the existing client.
        Otherwise, it creates a new client.

        Args:
            schema: The client data.

        Returns:
            The existing or newly created client schema.
        """
        if not schema.email:
            logger.error("Email is required to get or create a client.")
            raise ValueError("Email is required to get or create a client.")

        # Type hint for clarity
        repo: ClientRepository = self._repository

        # Check if client with this email already exists
        existing_client_model = repo.find_by_email(schema.email)

        if existing_client_model:
            logger.info(f"Client with email {schema.email} already exists. Returning existing client.")
            # Convert the existing ORM model to a Pydantic schema before returning
            
            return self._schema.model_validate(existing_client_model)
        
        logger.info(f"No client found with email {schema.email}. Creating a new client.")
        # If not found, use the generic save method from the base class to create a new one
        return super().save(schema)
