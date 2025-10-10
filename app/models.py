from datetime import datetime
from sqlalchemy import (Column, Integer, String,
                        DateTime, Float, ForeignKey, Index)
from sqlalchemy.orm import relationship

from .database import Base


class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    additional_info = Column(String(1024), nullable=True)

    temperatures = relationship(
        "Temperature",
        back_populates="city",
        cascade="all, delete"
    )

    def __repr__(self) -> str:
        return f"<City id={self.id} name={self.name!r}>"


class Temperature(Base):
    __tablename__ = "temperatures"
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(
        Integer,
        ForeignKey("cities.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    date_time = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )
    temperature = Column(Float, nullable=False)

    city = relationship("City", back_populates="temperatures")

    __table_args__ = (
        Index("ix_temperatures_city_time", "city_id", "date_time"),
    )

    def __repr__(self) -> str:
        return (f"<Temperature id={self.id} "
                f"city_id={self.city_id} "
                f"t={self.temperature} "
                f"at={self.date_time}>")
