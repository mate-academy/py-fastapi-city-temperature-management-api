from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship

from database import Base


class DBTemperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("city.id"))
    date_time = Column(DateTime, default=datetime.utcnow())
    temperature = Column(Float)

    city = relationship("DBCity", back_populates="temperatures", lazy="select")
