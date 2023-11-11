from fastapi import APIRouter, Depends, HTTPException , Query
from sqlalchemy.orm import Session
from db.base import get_db
from models.sale import Sale
from models.category import Category
from schemas.revenue import  RevenueComparisonRequest
from models.product import Product
from sqlalchemy import func
from typing import List

router = APIRouter()

# get revenuw on daily , monthly , weekly and anually
@router.get("/revenue", response_model=dict)
def get_revenue_analysis(
    interval: str = Query(..., description="Interval for revenue analysis (daily, weekly, monthly, annual)"),
    db: Session = Depends(get_db)
):
    valid_intervals = ["daily", "weekly", "monthly", "annual"]
    if interval not in valid_intervals:
        raise HTTPException(status_code=400, detail="Invalid interval. Allowed values: daily, weekly, monthly, annual")

    date_format_function = {
        "daily": func.DATE_FORMAT(Sale.sale_date, "%Y-%m-%d"),
        "weekly": func.DATE_FORMAT(Sale.sale_date, "%X-%V"),
        "monthly": func.DATE_FORMAT(Sale.sale_date, "%Y-%m"),
        "annual": func.DATE_FORMAT(Sale.sale_date, "%Y")
    }

    # Calculate revenue analysis
    revenue_analysis = (
        db.query(
            date_format_function[interval].label('date'),
            func.sum(Sale.amount).label('revenue'),
            Product.name.label('product_name')
        )
        .join(Product, Sale.product_id == Product.product_id)
        .group_by(date_format_function[interval], Product.name)
        .order_by(date_format_function[interval])
        .all()
    )

    # Calculate total revenue
    total_revenue = db.query(func.sum(Sale.amount)).scalar()

    # Prepare the response
    response_data = {
        "total_revenue": total_revenue,
        "revenue_analysis": [
            {"date": row.date, "revenue": row.revenue, "product_name": row.product_name} for row in revenue_analysis
        ]
    }

    return response_data


# compare revenue across different period and categories



@router.post("/revenue/comparison")
def compare_revenue(
    comparison_request: RevenueComparisonRequest,
    db: Session = Depends(get_db)
):
    start_date = comparison_request.start_date
    end_date = comparison_request.end_date
    category_ids = comparison_request.category_ids

    revenue_comparison = (
        db.query(
            func.sum(Sale.amount).label('revenue'),
            Product.category.label('category_id'),
            Category.cat_name.label('cat_name')
        )
        .join(Product, Sale.product_id == Product.product_id)
        .join(Category, Product.category == Category.category_id)
        .filter(Sale.sale_date >= start_date, Sale.sale_date <= end_date)
        .filter(Product.category.in_(category_ids))
        .group_by(Product.category)
        .all()
    )

    return [
        {"period": f"{start_date} to {end_date}", "category_id": row.category_id, "category_name": row.cat_name, "revenue": row.revenue}
        for row in revenue_comparison
    ]
