from db.engine import Base
from sqlalchemy import Column, Integer, String


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    additional_info = Column(String(555), nullable=False)
