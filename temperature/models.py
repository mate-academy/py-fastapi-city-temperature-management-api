from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    datetime = Column(DateTime, default=datetime.now)
    temperature = Column(Float)
    city_id = Column(Integer, ForeignKey("cities.id"))

    city = relationship("City", back_populates="temperatures")
