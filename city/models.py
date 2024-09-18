from sqlalchemy import (
    Column,
    Integer,
    String
)
from sqlalchemy.orm import relationship

from db.engine import Base


class City(Base):
    __tablename__ = "city"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    additional_info = Column(String)

    temperature = relationship("Temperature", back_populates="city")
