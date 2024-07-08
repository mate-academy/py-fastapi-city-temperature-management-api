from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float

from database import Base


class DBTemperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("city.id"), nullable=False)
    temperature = Column(Float, nullable=False)
    date_time = Column(DateTime, nullable=False)
