from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from city.models import City
from database import Base


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("city.id"))
    date_time = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    temperature = Column(Integer, nullable=False)

    city = relationship(City)
