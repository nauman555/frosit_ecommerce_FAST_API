from fastapi import APIRouter, Depends, HTTPException , Query
from sqlalchemy.orm import Session , joinedload
from db.base import get_db
from models.sale import Sale
from models.product import Product
from schemas.sale import SaleSchema
from datetime import date, timedelta
router = APIRouter()


@router.get("/sales")
def get_sales_data(
    start_date: date,
    end_date: date,
    product_id: int = None,
    category_id: int = None,
    db: Session = Depends(get_db)
):
    # Retrieve sales data within the specified date range
    query = (
        db.query(Sale, Product.name)
        .join(Product, Sale.product_id == Product.product_id)
        .filter(Sale.sale_date >= start_date, Sale.sale_date <= end_date)
    )

    # Apply additional filters for product and category if provided
    if product_id is not None:
        query = query.filter(Sale.product_id == product_id)

    if category_id is not None:
        query = query.filter(Sale.category_id == category_id)

    # Execute the final query and return the results
    sales_data = query.all()

    # Extract relevant information and create the response
    response_data = [
        {
            "sale_id": row.Sale.sale_id,
            "sale_date": row.Sale.sale_date,
            "amount": row.Sale.amount,
            "product_id": row.Sale.product_id,
            "category_id": row.Sale.category_id,
            "product_name": row.name,  # Include the product name
        }
        for row in sales_data
    ]

    return response_data
