from database import Base

from sqlalchemy import Column, Integer, String


class DBCity(Base):
    __tablename__ = "city"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    additional_info = Column(String(500))
