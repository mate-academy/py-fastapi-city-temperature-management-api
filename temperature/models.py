from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from city import models
from database import Base


class DBTemperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)

    city_id = Column(Integer, ForeignKey("city.id"))
    city = relationship(models.DBCity, back_populates="temperatures")

    date_time = Column(DateTime, nullable=False, server_default=func.now())
    temperature = Column(Float, nullable=False)

    @hybrid_property
    def formatted_date(self):
        return self.date_time.strftime("%Y-%m-%d")
