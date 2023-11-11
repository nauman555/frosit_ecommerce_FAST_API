from pydantic import BaseModel
from datetime import date

class SaleSchema(BaseModel):
    sale_id: int
    product_id: int
    category_id: int
    quantity: int
    amount: float
    sale_date: date
