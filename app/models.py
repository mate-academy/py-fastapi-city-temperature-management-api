from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    additional_info = Column(String, nullable=True)

    class Temperature(Base):
        __tablename__ = "temperatures"

        id = Column(Integer, primary_key=True, index=True)
        city_id = Column(Integer, ForeignKey("cities.id"))
        date_time = Column(DateTime, default=datetime.datetime.utcnow)
        temperature = Column(Float)
        city = relationship("City")
