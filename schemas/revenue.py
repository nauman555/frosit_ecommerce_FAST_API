from pydantic import BaseModel
from datetime import date
from typing import List

class RevenueAnalysisSchema(BaseModel):
    date: date
    revenue: float

class RevenueComparisonSchema(BaseModel):
    period: str
    category_id: int
    cat_name: str
    revenue: float

class RevenueComparisonRequest(BaseModel):
    start_date: date
    end_date: date
    category_ids: List[int]
