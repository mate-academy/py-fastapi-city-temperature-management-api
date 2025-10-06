from sqlalchemy import (
    Column,
    Integer,
    Float,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from city_temperature.database import Base
from datetime import (
    datetime,
    timezone,
)


class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    date_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    temperature = Column(Float, nullable=False)

    city = relationship("City", back_populates="temperatures")
