from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime)
    temperature = Column(Integer)
    city_id = Column(Integer, ForeignKey("city.id"))

    city = relationship("City", back_populates="temperatures")
