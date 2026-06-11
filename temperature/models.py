from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from database import Base


class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), index=True)
    date_time = Column(DateTime, index=True)
    temperature = Column(Float)
