from datetime import datetime, timezone

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship

from database import Base


class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer,
                     ForeignKey("cities.id"),
                     nullable=False,
                     index=True)
    date_time = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )
    temperature = Column(Float, nullable=False)

    city = relationship("City", back_populates="temperatures")
