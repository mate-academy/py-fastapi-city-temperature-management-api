from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("city.id"))
    date_time = Column(DateTime, nullable=True)
    temperature = Column(Float, nullable=False, default=date_time.now())

    city = relationship("City", back_populates="temperature")
