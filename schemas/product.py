from pydantic import BaseModel
from datetime import date

class ProductSchema(BaseModel):
    product_id: int
    name: str
    description: str
    price: float
    category: int
    created_at: date


class ProductCreateSchema(BaseModel):
    name: str
    description: str
    price: float
    category: int
    created_at: date
