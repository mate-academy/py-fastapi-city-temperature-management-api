from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class CityModels(Base):
    __tablename__ = "city"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    additional_info = Column(String)
    temperature = relationship("TemperatureModels", back_populates="city")