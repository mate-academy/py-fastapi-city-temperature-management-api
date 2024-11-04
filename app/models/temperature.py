import datetime

from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.core.database import Base


class Temperature(Base):
    __tablename__ = "temperatures"
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    date_time = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    temperature = Column(Float, nullable=False)
    city = relationship("City", back_populates="temperatures")
