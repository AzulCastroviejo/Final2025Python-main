"""Product service with Redis caching integration and sanitized logging."""
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select

from models.order_detail import OrderDetailModel
from models.product import ProductModel
from repositories.product_repository import ProductRepository
from schemas.product_schema import ProductSchema
from services.base_service_impl import BaseServiceImpl
from services.cache_service import cache_service
from utils.logging_utils import get_sanitized_logger

logger = get_sanitized_logger(__name__)


class ProductService(BaseServiceImpl):
    """Service for Product entity with caching."""

    def __init__(self, db: Session):
        super().__init__(
            repository_class=ProductRepository,
            model=ProductModel,
            schema=ProductSchema,
            db=db
        )
        self.cache = cache_service
        self.cache_prefix = "products"

    def get_products_by_category(self, category_id: int, skip: int = 0, limit: int = 100) -> List[ProductSchema]:
        """Get all products for a given category with caching."""
        cache_key = self.cache.build_key(self.cache_prefix, "category", category_id, skip=skip, limit=limit)
        cached_products = self.cache.get(cache_key)

        if cached_products is not None:
            logger.debug(f"Cache HIT: {cache_key}")
            return [ProductSchema(**p) for p in cached_products]

        logger.debug(f"Cache MISS: {cache_key}")
        # Corrected to call the right repository method
        products = self.repository.get_products_by_category(category_id, skip, limit)
        
        products_dict = [p.model_dump() for p in products]
        self.cache.set(cache_key, products_dict)

        return products

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ProductSchema]:
        """Get all products with caching."""
        cache_key = self.cache.build_key(self.cache_prefix, "list", skip=skip, limit=limit)
        cached_products = self.cache.get(cache_key)
        if cached_products is not None:
            logger.debug(f"Cache HIT: {cache_key}")
            return [ProductSchema(**p) for p in cached_products]

        logger.debug(f"Cache MISS: {cache_key}")
        products = super().get_all(skip, limit)
        products_dict = [p.model_dump() for p in products]
        self.cache.set(cache_key, products_dict)
        return products

    def get_one(self, id_key: int) -> ProductSchema:
        """Get single product by ID with caching."""
        cache_key = self.cache.build_key(self.cache_prefix, "id", id=id_key)
        cached_product = self.cache.get(cache_key)
        if cached_product is not None:
            logger.debug(f"Cache HIT: {cache_key}")
            return ProductSchema(**cached_product)

        logger.debug(f"Cache MISS: {cache_key}")
        product = super().get_one(id_key)
        self.cache.set(cache_key, product.model_dump())
        return product

    def save(self, schema: ProductSchema) -> ProductSchema:
        """Create new product and invalidate list caches."""
        product = super().save(schema)
        self._invalidate_caches()
        return product

    def update(self, id_key: int, schema: ProductSchema) -> ProductSchema:
        """Update product and invalidate relevant caches."""
        product = super().update(id_key, schema)
        cache_key = self.cache.build_key(self.cache_prefix, "id", id=id_key)
        self.cache.delete(cache_key)
        self._invalidate_caches()
        return product

    def delete(self, id_key: int) -> None:
        """Delete product with sales history validation and cache invalidation."""
        stmt = select(OrderDetailModel).where(OrderDetailModel.product_id == id_key).limit(1)
        has_sales = self.repository.session.scalars(stmt).first()

        if has_sales:
            logger.error(f"Cannot delete product {id_key}: has associated sales history")
            raise ValueError(
                f"Cannot delete product {id_key}: has associated sales history. "
                f"Consider marking as inactive instead of deleting."
            )

        super().delete(id_key)
        cache_key = self.cache.build_key(self.cache_prefix, "id", id=id_key)
        self.cache.delete(cache_key)
        self._invalidate_caches()

    def _invalidate_caches(self):
        """Invalidate all product list and category caches."""
        list_pattern = f"{self.cache_prefix}:list:*"
        category_pattern = f"{self.cache_prefix}:category:*"
        deleted_lists = self.cache.delete_pattern(list_pattern)
        deleted_categories = self.cache.delete_pattern(category_pattern)
        if deleted_lists > 0:
            logger.info(f"Invalidated {deleted_lists} product list cache entries")
        if deleted_categories > 0:
            logger.info(f"Invalidated {deleted_categories} product category cache entries")
