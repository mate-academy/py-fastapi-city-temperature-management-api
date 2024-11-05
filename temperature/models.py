from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from database import Base


class Temperature(Base):
    __tablename__ = "Temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("City.id"), nullable=False)
    date_time = Column(DateTime, default=datetime.utcnow)
    temperature = Column(Float, nullable=False)
