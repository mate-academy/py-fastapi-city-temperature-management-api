from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import Relationship

from db.engine import Base


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("city.id"), nullable=False)
    date_time = Column(DateTime, default=datetime.utcnow(), nullable=False)
    temperature = Column(Float, nullable=False)

    city = Relationship("City", back_populates="temperatures")
