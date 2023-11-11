from pydantic import BaseModel
from datetime import date

class InventorySchema(BaseModel):
    product_id: int
    quantity_available: int
    last_updated: date


class LowStockAlertSchema(BaseModel):
    product_id: int
    product_name: str
    quantity_available: int
    threshold: int
    is_low_stock: bool
