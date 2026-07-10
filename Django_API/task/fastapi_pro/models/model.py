from sqlalchemy import Column, String, Integer, ForeignKey
from databases.database import Base
import datetime


def timedate():
    dt = datetime.datetime.now()
    return dt

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    image = Column(String, nullable=False)
    category = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"))
    create_at = Column(String, default=timedate)