"""Product controller with category filtering endpoint."""
from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session

from config.database import get_db
from controllers.base_controller_impl import BaseControllerImpl
from schemas.product_schema import ProductSchema
from services.product_service import ProductService


class ProductController(BaseControllerImpl):
    """Controller for Product entity with CRUD operations and category filtering."""

    def __init__(self):
        super().__init__(
            schema=ProductSchema,
            service_factory=lambda db: ProductService(db),
            tags=["Products"]
        )
        # Add custom endpoint for fetching products by category
        @self.router.get("/category/{category_id}", 
                         response_model=List[ProductSchema],
                         summary="Get Products by Category ID",
                         description="Retrieve a paginated list of products belonging to a specific category.")
        async def get_products_by_category(
            category_id: int,
            skip: int = 0,
            limit: int = 100,
            db: Session = Depends(get_db)
        ):
            """Endpoint to get products by their category ID."""
            service = self.service_factory(db)
            return service.get_by_category_id(category_id, skip, limit)
