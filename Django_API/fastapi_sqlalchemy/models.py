from sqlalchemy import Column, Integer, String
from database import Base    # database vali file no base variable include karo

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    city = Column(String)