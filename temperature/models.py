from sqlalchemy import Column, Float, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone


class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("city.id"))
    date_time = Column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc)
    )
    temperature = Column(Float, nullable=False)

    city = relationship("City", back_populates="temperatures")
