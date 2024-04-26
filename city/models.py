from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class CityDB(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    additional_info = Column(String, nullable=True)
    temperatures = relationship("TemperatureDB", back_populates="city")
