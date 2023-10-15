from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from city.models import City
from database import Base


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime(timezone=True))
    temperature = Column(Integer, nullable=False)
    city_id = Column(Integer, ForeignKey("city.id"))

    city = relationship(City)
