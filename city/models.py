from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, FLOAT
from sqlalchemy.orm import relationship

from database import Base


class DBCity(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(63), nullable=False, unique=True)
    additional_info = Column(String(511), nullable=False)

    temperatures = relationship(
        "DBTemperature",
        back_populates="city",
        cascade="all, delete-orphan"
    )


class DBTemperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("city.id", ondelete="CASCADE"))
    date_time = Column(DateTime, nullable=False)
    temperature = Column(FLOAT, nullable=False)

    city = relationship(DBCity, back_populates="temperatures")
