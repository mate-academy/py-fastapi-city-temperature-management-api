from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Temperature(Base):
    __tablename__ = "temperature"
    id = Column(Integer, primary_key=True)
    temperature = Column(Float, nullable=False)
    date_time = Column(DateTime, nullable=False)
    city_id = Column(Integer, ForeignKey("city.id"))
    city = relationship("City", backref="temperature")
