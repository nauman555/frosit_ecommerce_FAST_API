from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from db.base import Base

class Sale(Base):
    __tablename__ = 'sales'

    sale_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'))
    category_id = Column(Integer, ForeignKey('categories.category_id'))
    quantity = Column(Integer)
    amount = Column(Float)
    sale_date = Column(Date)
