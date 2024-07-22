from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from database import Base


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float)
    date_time = Column(DateTime)
    city_id = Column(Integer, ForeignKey("city.id"))
    city = relationship("City")
