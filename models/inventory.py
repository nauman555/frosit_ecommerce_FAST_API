from sqlalchemy import Column, Integer, Date , ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base

class Inventory(Base):
    __tablename__ = 'inventory'

    product_id = Column(Integer, primary_key=True)
    quantity_available = Column(Integer)
    last_updated = Column(Date)



class InventoryHistory(Base):
    __tablename__ = 'inventory_history'

    history_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.product_id'))
    quantity_available = Column(Integer)
    last_updated = Column(Date)

    product = relationship('Product')
