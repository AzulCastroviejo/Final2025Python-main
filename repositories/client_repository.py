"""Client repository for database operations."""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from models.client import ClientModel
from repositories.base_repository_impl import BaseRepositoryImpl
from schemas.client_schema import ClientSchema


class ClientRepository(BaseRepositoryImpl):
    """Repository for Client entity database operations."""

    def __init__(self, db: Session):
        super().__init__(ClientModel, ClientSchema, db)
        
    def find_by_email(self, email: str) -> Optional[ClientModel]:
        """
        Find a client by their email address.

        Args:
            email: The email address to search for.

        Returns:
            The ClientModel if found, otherwise None.
        """
        stmt = select(self.model).where(self.model.email == email)
        client = self.session.scalars(stmt).first()
        return client
