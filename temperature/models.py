from sqlalchemy import Column, Integer, Date, Float, ForeignKey
from sqlalchemy.orm import relationship

from city.models import DBCity
from database import Base


class DBTemperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(Date)
    temperature = Column(Float)
    city_id = Column(Integer, ForeignKey("city.id"), nullable=False)

    city = relationship(DBCity)
