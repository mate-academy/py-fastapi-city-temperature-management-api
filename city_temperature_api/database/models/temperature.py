import datetime

from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from city_temperature_api.database.session.engine import Base


class Temperature(Base):

    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), index=True)
    date_time = Column(
        DateTime,
        default=datetime.datetime.now(datetime.UTC),
        nullable=False
    )
    temperature = Column(Float, nullable=False)

    city = relationship("City", back_populates="temperatures")
