from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float

from db import engine


Base = engine.Base


class Temperature(Base):
    __tablename__ = "temperatures"

    id: int = Column(Integer, primary_key=True, index=True)
    city_id: int = Column(ForeignKey("cities.id"))
    date_time: datetime = Column(DateTime, nullable=False)
    temperature: int = Column(Float, unique=False)
