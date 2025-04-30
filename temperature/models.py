from datetime import datetime, timezone

from sqlalchemy import Column, Float, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from database import Base


class TemperatureModel(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float, nullable=False)
    city_id = Column(Integer, ForeignKey("city.id"), nullable=False)
    date_time = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

    city = relationship("CityModel", back_populates="temperatures")

    __table_args__ = (
        UniqueConstraint('city_id', 'date_time', name='uq_city_date_time'),
    )
