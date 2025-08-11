from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from src.db import models
from src.db.engine import Base


class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime, nullable=False)
    temperature = Column(Integer, nullable=False)

    city_id = Column(Integer, ForeignKey("cities.id"))
    city = relationship(models.City)
