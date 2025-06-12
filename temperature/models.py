from sqlalchemy.orm import relationship

from database import Base
from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey


class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True)
    city_id = Column(
        Integer,
        ForeignKey("cities.id"),
        nullable=False,
        index=True
    )
    date_time = Column(DateTime, nullable=False)
    temperature = Column(Float, nullable=False)

    city = relationship("City", back_populates="temperatures")
