from sqlalchemy import Column, Integer, String

from database import Base

class DBCity(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    additional_info = Column(String(511))