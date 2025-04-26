from sqlalchemy import Column, Integer, Date, Float, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Weather(Base):
    __tablename__ = 'weather'

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("city.id"), nullable=False)
    city = relationship("City", back_populates="weather")
    date_time = Column(Date, nullable=False)
    temperature = Column(Float, nullable=False)
