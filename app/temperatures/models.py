from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer

from app.database import Base


class DBTemperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(
        Integer, ForeignKey("cities.id", ondelete="CASCADE"), nullable=False
    )
    date_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    temperature = Column(Float, nullable=False)
