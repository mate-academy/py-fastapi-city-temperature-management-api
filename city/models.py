from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class DBCity(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), nullable=False)
    additional_info = Column(String(255), nullable=False)

    temperature = relationship(
        "DBTemperature",
        back_populates="city",
        uselist=False
    )


class DBTemperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("city.id"))
    date_time = Column(DateTime)
    temperature = Column(Float, nullable=False)

    city = relationship("DBCity", back_populates="temperature", uselist=False)
