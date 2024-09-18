from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Float,
    DateTime
)
from sqlalchemy.orm import relationship

from db.engine import Base


class Temperature(Base):
    __tablename__ = "temperatures"
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("city.id"))
    date_time = Column(DateTime, default=datetime.now, nullable=False)
    temperature = Column(Float)

    city = relationship("City", back_populates="temperature")
