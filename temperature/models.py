import datetime

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    Float
)

from database import Base


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime, default=datetime.datetime.utcnow)
    temperature = Column(Float)
    city_id = Column(Integer, ForeignKey("city.id"))
