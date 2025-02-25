
from sqlalchemy import (
    Integer,
    Column,
    ForeignKey,
    DateTime,
    Float
)
from sqlalchemy.orm import relationship

from database import Base


class DBTemperature(Base):
    __tablename__ = "temperature"
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("city.id"), nullable=False)
    date_time = Column(DateTime, nullable=True)
    temperature = Column(Float, nullable=True)


city = relationship("DBCity", back_populates="temperatures")
