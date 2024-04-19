from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship

from database import Base


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    city_id = Column(Integer, ForeignKey("city.id"))
    temperature = Column(Float)
    date_time = Column(DateTime)

    city = relationship("City", back_populates="temperatures")
