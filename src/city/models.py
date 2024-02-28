from __future__ import annotations


from sqlalchemy import String, Column, Integer

from src.database import Base


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    additional_info = Column(String(500), nullable=True)
