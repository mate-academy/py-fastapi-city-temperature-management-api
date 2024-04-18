from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.database import Base


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime, index=True)
    temperature = Column(Float, index=True)
    city_id = Column(Integer, ForeignKey("city.id"))

    city = relationship("City", back_populates="temperatures")
