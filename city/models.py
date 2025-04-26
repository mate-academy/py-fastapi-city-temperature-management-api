from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), nullable=False, unique=True)
    additional_info = Column(String(100), nullable=False, unique=True)
    weather = relationship("Weather", back_populates="city")
