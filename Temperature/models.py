from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, Float
from sqlalchemy.orm import relationship

from database import Base
from City.models import DBCity

class Temperature(Base):
    __tablename__ = "temperature"
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("city.id"))
    city = relationship(DBCity)
    date_time = Column(DateTime(timezone=True), server_default=func.now())
    temperature = Column(Float)