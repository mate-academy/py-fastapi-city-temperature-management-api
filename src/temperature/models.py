from sqlalchemy import Column, Integer, DateTime, Float

from src.database import Base


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer)
    date_time = Column(DateTime)
    temperature = Column(Float)
