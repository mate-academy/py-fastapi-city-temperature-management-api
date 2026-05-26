from datetime import datetime, timezone

from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("city.id"))
    date_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    temperature = Column(Float, nullable=False)

    city = relationship("City")
