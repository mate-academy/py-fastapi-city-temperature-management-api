from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float

from database import Base


class TemperatureModel(Base):
    __tablename__ = "temperature"
    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey("city.id"))
    date_time = Column(DateTime)
    temperature = Column(Float)
