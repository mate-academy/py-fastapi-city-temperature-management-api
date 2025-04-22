from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from.database import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    country = Column(String)
    temperatures = relationship("Temperature", back_populates="city", cascade="all, delete")


class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float)
    unit = Column(String, nullable=False)
    city_id = Column(Integer, ForeignKey("cities.id"))

    city = relationship("City", back_populates="temperatures")
