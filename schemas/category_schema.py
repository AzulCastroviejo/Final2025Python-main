"""Category schema with validation."""
from typing import Optional, TYPE_CHECKING
from pydantic import Field
#, List, TYPE_CHECKING
from schemas.base_schema import BaseSchema

#if TYPE_CHECKING:
 #   from schemas.product_schema import ProductSchema


class CategorySchema(BaseSchema):
    """Schema for Category entity with validations.

    The list of products is intentionally omitted to prevent circular dependencies
    when this schema is nested within others (e.g., in ProductSchema).
    """

    name: str = Field(..., min_length=1, max_length=100, description="Category name (required, unique)")

    # ✅ AGREGAR description
    description: Optional[str] = Field(None, max_length=500, description="Category description")


   # products: Optional[List['ProductSchema']] = []


