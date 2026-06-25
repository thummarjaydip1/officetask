from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from database.database import Base
from datetime import datetime
import pytz

def india_time():
    return datetime.now(pytz.timezone("Asia/Kolkata"))

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    username = Column(String, nullable = False)
    password = Column(String, nullable = False)
    email = Column(String, nullable = False, unique = True)
    address = Column(String, nullable = True)
    image = Column(String, nullable=False)
    create_at = Column(DateTime, default = india_time)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key = True)
    name = Column(String, nullable=False)
    price = Column(String, nullable=False)
    image = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey('products.id', ondelete="CASCADE")) 
    quantity = Column(Integer, default=1, nullable=False)
    total = Column(Integer, nullable=False)


class Wishlist(Base):
    __tablename__ = "wishlists"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    quantity = Column(Integer, default=1, nullable=False)
    total = Column(Integer, nullable=False)

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    message = Column(Integer, nullable=False)