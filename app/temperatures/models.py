from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    date_time = Column(DateTime, default=datetime.utcnow)
    temperature = Column(Float)
    city = relationship("City")
