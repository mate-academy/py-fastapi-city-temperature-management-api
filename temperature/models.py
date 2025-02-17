from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship

from database import Base


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(
        Integer,
        ForeignKey("city.id"),
        nullable=False,
        unique=True
    )
    date_time = Column(DateTime, nullable=False)
    temperature = Column(String, nullable=False)

    city = relationship("City", back_populates="temperatures")
