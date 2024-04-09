from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship
from database import Base


class DBTemperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Numeric, nullable=False)
    data_time = Column(DateTime, default=datetime.utcnow, nullable=True)
    city_id = Column(Integer, ForeignKey("city.id"))
    city = relationship("DBCity", back_populates="temperatures")
