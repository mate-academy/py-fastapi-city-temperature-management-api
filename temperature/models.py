import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship

from city.models import DBCity
from database import Base


class DBTemperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    date_time = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow
    )
    temperature = Column(DECIMAL, nullable=False)

    city = relationship(DBCity)
