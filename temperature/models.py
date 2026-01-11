from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship

from database import Base


class Temperature(Base):
    __tablename__ = "Temperature"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime, nullable=False)
    temperature = Column(Float, nullable=False)
    city_id = Column(Integer, ForeignKey("City.id"), nullable=False)

    city = relationship("City", back_populates="temperatures")