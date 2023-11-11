from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.base import get_db
from models.inventory import Inventory, InventoryHistory
from models.product import Product
from schemas.inventory import InventorySchema, LowStockAlertSchema

router = APIRouter()


# get all inventory details
@router.get("/inventory")
def get_all_inventory_data(db: Session = Depends(get_db)):
    query_result = (
        db.query(Inventory, Product)
        .join(Product, Inventory.product_id == Product.product_id)
        .all()
    )

    inventory_with_product_name = [
        {
            "product_id": inventory.Product.product_id,
            "product_name": inventory.Product.name,
            "quantity_available": inventory.Inventory.quantity_available,
            "last_updated": inventory.Inventory.last_updated,
        }
        for inventory in query_result
    ]

    return inventory_with_product_name


# get inventory details with product id

@router.get("/inventory/{product_id}")
def get_inventory_by_product_id(product_id: int, db: Session = Depends(get_db)):
    query_result = (
        db.query(Inventory, Product)
        .join(Product, Inventory.product_id == Product.product_id)
        .filter(Inventory.product_id == product_id)
        .first()
    )

    if query_result is None:
        raise HTTPException(status_code=404, detail="Inventory not found")

    inventory, product = query_result

    inventory_with_product_name = {
        "product_id": product.product_id,
        "product_name": product.name,
        "quantity_available": inventory.quantity_available,
        "last_updated": inventory.last_updated,
    }

    return inventory_with_product_name


# update the inventory quantity

@router.put("/inventory/{product_id}", response_model=InventorySchema)
def update_inventory(product_id: int, quantity: int, db: Session = Depends(get_db)):
    # Get the current inventory entry
    inventory_entry = db.query(Inventory).filter(Inventory.product_id == product_id).first()

    if inventory_entry:
        # Update existing inventory entry
        inventory_entry.quantity_available = quantity
        inventory_entry.last_updated = date.today()

        # Log the change in the history table
        inventory_history_entry = InventoryHistory(
            product_id=inventory_entry.product_id,
            quantity_available=inventory_entry.quantity_available,
            last_updated=inventory_entry.last_updated
        )
        db.add(inventory_history_entry)

    else:
        # Create a new inventory entry if none exists
        inventory_entry = Inventory(
            product_id=product_id,
            quantity_available=quantity,
            last_updated=date.today()
        )
        db.add(inventory_entry)

    db.commit()
    db.refresh(inventory_entry)
    return inventory_entry


# get the inventory update histroy
@router.get("/inventory/history/{product_id}")
def get_inventory_update_history_by_product_id(product_id: int, db: Session = Depends(get_db)):
    query_result = (
        db.query(InventoryHistory, Product)
        .join(Product, InventoryHistory.product_id == Product.product_id)
        .filter(InventoryHistory.product_id == product_id)
        .all()
    )

    if not query_result:
        return []

    inventory_history_with_product_name = [
        {
            "history_id": history.history_id,
            "product_id": history.product_id,
            "product_name": product.name,
            "quantity_available": history.quantity_available,
            "last_updated": history.last_updated,
        }
        for history, product in query_result
    ]

    return inventory_history_with_product_name


# get the loq stock inveroty data
# we have set by default low stock quantity value 10
# we can call this API when the admin logged in to the admin dashboard or we can set cron job to run the API daily


@router.get("/inventory/low_stock_alerts/{threshold}")
def get_low_stock_alerts(threshold:int, db: Session = Depends(get_db)):
    try:
        threshold = int(threshold)  # Explicitly convert to an integer
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid threshold value. Must be an integer.")

    query_result = (
        db.query(Inventory, Product)
        .join(Product, Inventory.product_id == Product.product_id)
        .filter(Inventory.quantity_available <= threshold)
        .all()
    )
    low_stock_alerts = [
        {
            "product_id": inventory.product_id,
            "product_name": product.name,
            "quantity_available": inventory.quantity_available,
            "threshold": threshold,
            "is_low_stock": inventory.quantity_available <= threshold,
        }
        for inventory, product in query_result
    ]

    return low_stock_alerts
