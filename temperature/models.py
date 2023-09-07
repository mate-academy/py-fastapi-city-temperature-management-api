from sqlalchemy.orm import relationship

from engine import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float


class DBTemperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(DateTime, ForeignKey("cities.id"))
    date_time = Column(DateTime)
    temperature = Column(Float)

    city = relationship("City", back_populates="temperatures")

