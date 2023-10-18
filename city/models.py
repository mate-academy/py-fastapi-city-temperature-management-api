from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class DBCity(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(68), nullable=False)
    additional_info = Column(String(511))

    temperatures = relationship("DBTemperature", back_populates="city")
