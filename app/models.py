from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    func,
    Float
)
from sqlalchemy.orm import relationship

from app.database import Base


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    additional_info = Column(String(510), nullable=True)

    temperatures = relationship(
        "Temperature",
        back_populates="city",
        cascade="all, delete-orphan"
    )


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey("city.id"), nullable=False)
    date_time = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    temperature = Column(Float, nullable=False)

    city = relationship("City", back_populates="temperatures")
