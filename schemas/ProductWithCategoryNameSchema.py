

class ProductWithCategoryNameSchema(BaseSchema):

    name: str
    price: float
    stock: int
    category_id: int
    category_name: str  # ✅ Solo el nombre, no el objeto completo