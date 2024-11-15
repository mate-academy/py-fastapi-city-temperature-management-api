from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    Float,
    CheckConstraint
)
from sqlalchemy.orm import relationship

from cities.models import DBCity
from cities.models import BaseClass


class Temperature(BaseClass):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    date_time = Column(DateTime, nullable=False)
    temperature = Column(Float, nullable=False)

    __table_args__ = (
        CheckConstraint(temperature >= -50.0, name="temperature_min_check"),
        CheckConstraint(temperature <= 70.0, name="temperature_max_check"),
    )

    city = relationship(DBCity)
