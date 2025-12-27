"""Centralized module for importing and resolving all Pydantic schemas."""

# Import all schemas to ensure they are in the module's scope
from .address_schema import AddressSchema
from .bill_schema import BillSchema
from .category_schema import CategorySchema
from .client_schema import ClientSchema
from .order_detail_schema import OrderDetailSchema
from .order_schema import OrderSchema
from .product_schema import ProductSchema
from .review_schema import ReviewSchema

# List of all schema classes to iterate over
ALL_SCHEMAS = [
    AddressSchema,
    BillSchema,
    CategorySchema,
    ClientSchema,
    OrderDetailSchema,
    OrderSchema,
    ProductSchema,
    ReviewSchema,
]

# Resolve all forward references
# This is the modern equivalent of the deprecated update_forward_refs()
for schema in ALL_SCHEMAS:
    schema.model_rebuild()

# You can also selectively export schemas if you prefer
__all__ = [
    "AddressSchema",
    "BillSchema",
    "CategorySchema",
    "ClientSchema",
    "OrderDetailSchema",
    "OrderSchema",
    "ProductSchema",
    "ReviewSchema",
]

