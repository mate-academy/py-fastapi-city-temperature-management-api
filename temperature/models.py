from sqlalchemy import (
    Column,
    Integer,
    Float,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship

from project_engine.database import Base


class DBTemperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("city.id"))
    date_time = Column(DateTime)
    # temperature in Celsius
    temp_c = Column(Float)
    # temperature in Fahrenheit
    temp_f = Column(Float)
    # define relationship with DBCity model
    city = relationship("DBCity", back_populates="temperatures")
