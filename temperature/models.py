from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship

from datetime import datetime
from database import Base


class DBTemperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("city.id"), nullable=False)
    date_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    temperature = Column(Float, nullable=False)

    city = relationship("DBCity", back_populates="temperatures")
