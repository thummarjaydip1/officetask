from sqlalchemy import String, Column, Integer
from database.database import Base

class Bill(Base):

    __tablename__ = "bills"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer)
    customer_name = Column(String)
    product_name = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)
    total_price = Column(Integer)

class Notification(Base):
    
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    message = Column(String)