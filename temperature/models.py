from sqlalchemy import DateTime, Column, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship

from city.models import City
from database import Base


class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime)
    temperature = Column(Numeric(precision=5, scale=2))
    city_id = Column(Integer, ForeignKey("cities.id"))

    city = relationship(City)
