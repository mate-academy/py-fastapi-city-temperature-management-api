from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship

from database import Base


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime)
    city_id = Column(Integer, ForeignKey("city.id"))
    temperature = Column(Float)

    city = relationship("City", back_populates="temperature")
