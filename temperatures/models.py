from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship

from database import Base


class DBTemperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    city = relationship("DBCity", back_populates="temperatures")
    date_time = Column(DateTime)
    temperature = Column(Float)
