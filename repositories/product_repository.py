"""Product repository for database operations."""
from sqlalchemy.orm import Session

from models.product import ProductModel
from repositories.base_repository_impl import BaseRepositoryImpl
from schemas.product_schema import ProductSchema


class ProductRepository(BaseRepositoryImpl):
    """Repository for Product entity database operations."""

    def __init__(self, db: Session):
        super().__init__(ProductModel, ProductSchema, db)


    def find_all(self, skip: int = 0, limit: int = 100):
        """Get all products with their categories loaded."""
        models = (
            self._session.query(self._model)
            .options(joinedload(ProductModel.category))
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._schema.model_validate(model) for model in models]

    def find_by_id(self, id_key: int):
        """Get a product by ID with category loaded."""
        model = (
            self._session.query(self._model)
            .options(joinedload(ProductModel.category))
            .filter(self.model.id_key == id_key)
            .first()
        )
        if model:
            return self._schema.model_validate(model)
        return None