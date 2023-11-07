from sqlalchemy import Column, Integer, String

from engine import Base


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(63), nullable=False, unique=True)
    additional_info = Column(String(255), nullable=True)
