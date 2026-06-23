from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String

from app.database import Base


class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    additional_info = Column(String)


class Temperature(Base):
    __tablename__ = "temperatures"
    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    date_time = Column(DateTime)
    temperature = Column(Float)
