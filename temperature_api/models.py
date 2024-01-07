from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, Float
from sqlalchemy.orm import relationship

from database import Base


class DBTemperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("city.id"))
    date_time = Column(
        DateTime(timezone=True), nullable=False, default=func.now()
    )
    temperature = Column(Float, nullable=False)

    city = relationship("DBCity", back_populates="temperature")
