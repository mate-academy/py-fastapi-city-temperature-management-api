from sqlalchemy import Column, ForeignKey, Integer, DateTime, Float
from sqlalchemy.orm import relationship

from database import Base
from city_data import models as city_models


class DBTemperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime, nullable=False)
    temperature = Column(Float, nullable=False)
    city_id = Column(
        Integer,
        ForeignKey("cities.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    city = relationship(city_models.DBCity)
