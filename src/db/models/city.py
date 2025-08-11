from sqlalchemy import Column, Integer, String

from src.db.engine import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    additional_info = Column(String(512))
