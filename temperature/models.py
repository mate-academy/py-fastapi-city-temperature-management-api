from database import Base

from sqlalchemy import Integer, Column, ForeignKey, DateTime


class DBTemperature(Base):
    __tablename__ = "temperature"
    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey("temperature.id"))
    date_time = Column(DateTime)
    temperature = Column(Integer)
