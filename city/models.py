from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from temperature import models
from database import Base


class DBCity(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    additional_info = Column(String(500))
    temperature = relationship("DBTemperature", back_populates="city")
