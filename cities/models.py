from sqlalchemy import Column, Integer, String

from db.engine import BaseClass


class DBCity(BaseClass):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    additional_info = Column(String(500), nullable=True)
