from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    additional_info = Column(String, index=True)


class Temperature(Base):
    __tablename__ = "temperatures"
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    date_time = Column(DateTime, index=True)
    temperature = Column(Float, index=True)
    city = relationship("City", back_populates="temperatures")


City.temperatures = relationship(
    "Temperature", order_by=Temperature.id, back_populates="city"
)
