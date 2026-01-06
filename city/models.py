import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from database import Base


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    additional_info = Column(String(500))
    temperature = relationship(
        "Temperature",
        back_populates="city",
        cascade="all, delete",
    )


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(
        Integer,
        ForeignKey("city.id"),
        index=True
    )
    date_time = Column(DateTime, default=datetime.datetime.now)
    temperature = Column(Float)

    city = relationship("City", back_populates="temperature")
