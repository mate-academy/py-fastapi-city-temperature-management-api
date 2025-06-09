from src.database import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.cities.models import City


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("city.id"))
    date_time = Column(DateTime, nullable=False)
    temperature =Column(Float, nullable=False)

    city = relationship("City", back_populates="temperatures")
