from typing import List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from models.product import ProductModel
from repositories.base_repository_impl import BaseRepositoryImpl


class ProductRepository(BaseRepositoryImpl):
    def __init__(self, db: Session):
        super().__init__(ProductModel, db)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ProductModel]:
        return (
            self.session.query(self.model)
            .options(joinedload(self.model.category))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_one(self, id_key: int) -> ProductModel | None:
        return (
            self.session.query(self.model)
            .options(joinedload(self.model.category))
            .filter(self.model.id_key == id_key)
            .first()
        )

    def get_products_by_category(
        self, category_id: int, skip: int, limit: int
    ) -> List[ProductModel]:
        stmt = (
            select(self.model)
            .options(joinedload(self.model.category))
            .where(self.model.category_id == category_id)
            .offset(skip)
            .limit(limit)
        )
        return self.session.scalars(stmt).all()
