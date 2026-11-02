from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database import Base


class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False, index=True)
    date_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    temperature = Column(Float, nullable=False)

    city = relationship("City", back_populates="temperatures")
