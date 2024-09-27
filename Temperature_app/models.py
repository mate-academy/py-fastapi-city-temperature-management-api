from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now

from project_settings.database import Base


class DBTemperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("city.id", ondelete="CASCADE"))
    date_time = Column(DateTime(timezone=True), default=now())
    temperature = Column(Float)
    city = relationship("DBCity", back_populates="temperatures")
