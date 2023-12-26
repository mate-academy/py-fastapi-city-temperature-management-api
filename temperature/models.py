from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import Column, ForeignKey, Integer, DateTime


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey("city.id"))
    date_time = Column(DateTime)
    temperature = Column(Integer)
    city = relationship("City", back_populates="temperature")
