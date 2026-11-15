from sqlalchemy import Column, Integer, String

from app.database import Base


class DBCity(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    additional_info = Column(String(500), nullable=True)
