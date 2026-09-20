from app.database import Base
from sqlalchemy import Column, String, Date, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship


class CityDB(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    additional_info = Column(String)

    temperatures = relationship("TemperatureDB", back_populates="city")


class TemperatureDB(Base):
    __tablename__ = "temperatures"
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    date_time = Column(Date)
    temperature = Column(Float)

    city = relationship("CityDB", back_populates="temperatures")
