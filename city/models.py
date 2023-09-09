from sqlalchemy.orm import relationship

from engine import Base
from sqlalchemy import Column, Integer, String
from temperature.models import DBTemperature


class DBCity(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(127), nullable=False, unique=True)
    additional_info = Column(String, nullable=False, unique=False)

    temperatures = relationship(DBTemperature, back_populates="city")
