from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.db.engine import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255),nullable=False, unique=True)
    additional_info = Column(String(511), nullable=False)
    temperatures = relationship("Temperature",
                                back_populates='cities')


class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(Date, nullable=False)
    temperature = Column(Integer, nullable=False)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=True)
    city = relationship(City, back_populates="temperatures")
