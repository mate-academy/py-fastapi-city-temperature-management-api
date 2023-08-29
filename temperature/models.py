from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from database import Base


class DBTemperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime)
    temperature = Column(Float)
    city_id = Column(Integer, ForeignKey("city.id"), nullable=False)

    city = relationship("DBCity", back_populates="temperature")
