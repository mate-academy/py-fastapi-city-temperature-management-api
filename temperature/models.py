from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, DateTime, Float

from database import Base


class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime, index=True, default=datetime.utcnow)
    temperature = Column(Float, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
