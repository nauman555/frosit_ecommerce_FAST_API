from sqlalchemy import Column, Integer, String, Date , Float
from db.base import Base

class Category(Base):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True)
    cat_name = Column(String)


