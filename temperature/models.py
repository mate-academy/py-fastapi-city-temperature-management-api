from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey, func
from sqlalchemy.orm import relationship

from database import Base


class DBTemperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime, server_default=func.now())
    temperature = Column(Float)
    city_id = Column(Integer, ForeignKey("city.id"))

    city = relationship("DBCity")
