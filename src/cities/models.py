from sqlalchemy import Column, Integer, String

from src.database import Base


class DBCity(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    additional_info = Column(String, nullable=True)
