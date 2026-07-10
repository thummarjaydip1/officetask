from sqlalchemy import Column, Integer, String
from databases.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    image = Column(String, nullable=False)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String, nullable=False)
    city = Column(String, nullable=False)