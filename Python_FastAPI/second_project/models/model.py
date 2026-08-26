from sqlalchemy import Column, String, Integer, ForeignKey
from databases.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    image = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"))


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, default=1)
    total_price = Column(Integer)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))