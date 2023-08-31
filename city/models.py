from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class DBCity(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, unique=True)
    additional_info = Column(String(500))

    temperatures = relationship("DBTemperature", back_populates="city")
