from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship

from database import Base

from temperatures.models import DBTemperature


class DBCity(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    additional_info = Column(String(500), nullable=True)
    temperatures = relationship("DBTemperature", back_populates="city")
