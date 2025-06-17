from datetime import datetime, UTC

from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    Float,
    ForeignKey,
    DateTime,
)

from database import Base


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    date_time = Column(DateTime, default=lambda: datetime.now(UTC))
    temperature = Column(Float)

    city = relationship("City")
