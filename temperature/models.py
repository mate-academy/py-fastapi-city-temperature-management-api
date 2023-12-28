from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from city.models import DBCity


class DBTemperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime, nullable=False)
    temperature = Column(Float(precision=2, asdecimal=True), nullable=False)
    city_id = Column(Integer, ForeignKey(DBCity.id))
    city = relationship(DBCity, uselist=True)
