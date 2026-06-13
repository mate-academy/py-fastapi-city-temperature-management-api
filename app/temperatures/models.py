from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id", ondelete="CASCADE"), nullable=False)
    date_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    temperature = Column(Float, nullable=False)

    city = relationship("app.cities.models.City", back_populates="temperatures")
