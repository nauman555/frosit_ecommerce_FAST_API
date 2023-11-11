from sqlalchemy import Column, Integer, String, Date , Float
from db.base import Base

class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    category = Column(Integer)
    created_at = Column(Date)

