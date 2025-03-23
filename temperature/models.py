from datetime import datetime

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from database import Base


class Temperature(Base):
    __tablename__ = "temperature"

    id: int = Column(Integer, primary_key=True, index=True)
    date_time: datetime = Column(DateTime, nullable=False, default=func.now())
    temperature: float = Column(Float, nullable=False)
    city_id: int = Column(
        Integer,
        ForeignKey("city.id", ondelete="CASCADE"),
        nullable=False
    )

    city = relationship("City", back_populates="temperature")
