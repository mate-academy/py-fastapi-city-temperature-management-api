from sqlalchemy.orm import relationship

from engine import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float


class DBTemperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    date_time = Column(DateTime)
    temperature = Column(Float)

    city = relationship("DBCity", back_populates="temperatures")
