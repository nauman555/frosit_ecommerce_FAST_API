from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.base import get_db
from models.product import Product
from schemas.product import ProductSchema
from schemas.product import ProductCreateSchema

router = APIRouter()


# get all products
# @router.get("/products", response_model=list[ProductSchema])
# def get_products(db: Session = Depends(get_db)):
#     products = db.query(Product).all()
#     return products


# API for add new product

@router.post("/add_product", response_model=ProductCreateSchema)
def create_product(
    product_data: ProductCreateSchema,
    db: Session = Depends(get_db)
):
    # check whether the product already exists / if the product already exists thn the admin should update the product quantity using update inventory API
    existing_product = db.query(Product).filter(Product.name == product_data.name).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="Product with this name already exists , please update the product quantity using update inventory method ")
    # currently we have only two categories 1 for Mobile and 2 for Laptops

    valid_cat_id = [1,2]
    if product_data.category not in valid_cat_id:
        raise HTTPException(status_code=400, detail="Invalid Category ID. Allowed values: 1 for Mobile Phones and 2 for Laptops")



    # Create the new product
    new_product = Product(**product_data.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product
