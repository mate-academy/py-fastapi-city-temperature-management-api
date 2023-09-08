from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, Float
from sqlalchemy.orm import relationship

from city.models import City
from database import Base


class Temperature(Base):
    __tablename__ = "temperature"
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("city.id"))
    date_time = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    temperature = Column(Float, nullable=False)

    city = relationship(City)
