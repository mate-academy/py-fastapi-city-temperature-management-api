from sqlalchemy import Column, ForeignKey, Integer, DateTime, Float
from sqlalchemy.orm import relationship

from database import Base


class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True)
    temperature = Column(Float, index=True, nullable=True)
    date_time = Column(DateTime, nullable=True)
    city_id = Column(Integer, ForeignKey("cities.id"))

    city = relationship("City", uselist=False)
