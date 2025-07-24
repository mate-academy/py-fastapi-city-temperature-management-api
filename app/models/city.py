# models/city.py
from sqlalchemy import Column, Integer, String
from app.db import Base

class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    additional_info = Column(String)
