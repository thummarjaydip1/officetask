from sqlalchemy import Column, String, Integer, Date
from databases.database import Base

class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    address = Column(String)
    birth_date = Column(Date, nullable=False)