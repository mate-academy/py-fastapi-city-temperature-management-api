from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from engine import Base
from city import models


class DBTemperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_name = Column(String, ForeignKey("city.name"))
    date_time_utc = Column(DateTime)
    temperature = Column(String(25), nullable=False)

    city = relationship(models.DBCity)
