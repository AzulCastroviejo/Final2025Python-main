"""
BaseRepository implementation with corrected return types and loading options.
"""
import logging
from typing import Type, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from models.base_model import BaseModel
from repositories.base_repository import BaseRepository
from schemas.base_schema import BaseSchema
from utils.logging_utils import get_sanitized_logger


class InstanceNotFoundError(Exception):
    """Raised when a database record is not found."""
    pass


class BaseRepositoryImpl(BaseRepository):
    """
    Generic repository implementation with SQLAlchemy 2.0 patterns.
    """

    def __init__(self, model: Type[BaseModel], schema: Type[BaseSchema], db: Session):
        self._model = model
        self._schema = schema
        self._session = db
        self.logger = get_sanitized_logger(__name__)

    @property
    def session(self) -> Session:
        return self._session

    @property
    def model(self) -> Type[BaseModel]:
        return self._model

    @property
    def schema(self) -> Type[BaseSchema]:
        return self._schema

    def find(self, id_key: int, load_options: Optional[List] = None) -> BaseModel:
        """
        Find a single record by ID, with optional relationship loading.
        """
        try:
            stmt = select(self.model)
            if load_options:
                stmt = stmt.options(*load_options)
            
            stmt = stmt.where(self.model.id_key == id_key)
            model = self.session.scalars(stmt).first()

            if model is None:
                raise InstanceNotFoundError(
                    f"{self.model.__name__} with id {id_key} not found"
                )

            return model
        except InstanceNotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"Error finding {self.model.__name__} with id {id_key}: {e}")
            raise

    def find_all(self, skip: int = 0, limit: int = 100, load_options: Optional[List] = None) -> List[BaseModel]:
        """
        Find all records with pagination and optional relationship loading.
        """
        from config.constants import PaginationConfig
        try:
            if skip < 0:
                raise ValueError("skip parameter must be >= 0")
            if limit < PaginationConfig.MIN_LIMIT:
                raise ValueError(f"limit must be >= {PaginationConfig.MIN_LIMIT}")
            if limit > PaginationConfig.MAX_LIMIT:
                limit = PaginationConfig.MAX_LIMIT

            stmt = select(self.model)
            # --- ¡AQUÍ ESTÁ LA LÍNEA QUE FALTABA! ---
            if load_options:
                stmt = stmt.options(*load_options)

            stmt = stmt.offset(skip).limit(limit)
            models = self.session.scalars(stmt).all()
            return models
        except ValueError:
            raise
        except Exception as e:
            self.logger.error(f"Error finding all {self.model.__name__}: {e}")
            raise

    def save(self, model: BaseModel) -> BaseModel:
        """
        Save a new record. Returns the new ORM model.
        """
        try:
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)
            return model
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Error saving {self.model.__name__}: {e}")
            raise

    def update(self, id_key: int, changes: dict) -> BaseModel:
        """
        Update an existing record. Returns the updated ORM model.
        """
        PROTECTED_ATTRIBUTES = {'id_key', '_sa_instance_state'}
        try:
            instance = self.find(id_key)

            allowed_columns = {col.name for col in self.model.__table__.columns}
            for key, value in changes.items():
                if value is None or key.startswith('_') or key in PROTECTED_ATTRIBUTES:
                    continue
                if key not in allowed_columns:
                    raise ValueError(f"Invalid field for {self.model.__name__}: {key}")
                setattr(instance, key, value)

            self.session.commit()
            self.session.refresh(instance)
            return instance
        except (InstanceNotFoundError, ValueError) as err:
            self.session.rollback()
            self.logger.error(f"Error updating {self.model.__name__} {id_key}: {err}")
            raise
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Error updating {self.model.__name__} {id_key}: {e}")
            raise

    def remove(self, id_key: int) -> None:
        """
        Delete a record from the database.
        """
        try:
            model = self.find(id_key)
            self.session.delete(model)
            self.session.commit()
        except InstanceNotFoundError:
            raise
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Error deleting {self.model.__name__} {id_key}: {e}")
            raise

    def save_all(self, models: List[BaseModel]) -> List[BaseModel]:
        """
        Save multiple records. Returns a list of the new ORM models.
        """
        try:
            self.session.add_all(models)
            self.session.commit()
            for model in models:
                self.session.refresh(model)
            return models
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Error saving multiple {self.model.__name__}: {e}")
            raise
