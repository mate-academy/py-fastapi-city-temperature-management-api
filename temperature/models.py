from db.engine import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from city.models import City


class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime, nullable=False)
    temperature = Column(String(255), nullable=False)

    city_id = Column(Integer, ForeignKey("cities.id"))

    city = relationship(City)
