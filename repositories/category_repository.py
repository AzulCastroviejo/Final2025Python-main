"""Category repository for database operations."""
from sqlalchemy.orm import Session, joinedload

from models.category import CategoryModel
from repositories.base_repository_impl import BaseRepositoryImpl
from schemas.category_schema import CategorySchema


class CategoryRepository(BaseRepositoryImpl):
    """Repository for Category entity database operations."""

    def __init__(self, db: Session):
        super().__init__(model=CategoryModel, schema=CategorySchema, db=db)


    def find_all(self, skip: int = 0, limit: int = 100):
        """Get all categories with their products loaded."""
        models = (
            self.db.query(self.model)
            .options(joinedload(CategoryModel.products))
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self.schema.model_validate(model) for model in models]

    def find_by_id(self, id_key: int):
        """Get a category by ID with products loaded."""
        model = (
            self.db.query(self.model)
            .options(joinedload(CategoryModel.products))
            .filter(self.model.id_key == id_key)
            .first()
        )
        if model:
            return self.schema.model_validate(model)
        return None