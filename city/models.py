from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class DBCity(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    additional_info = Column(String(1111))

    temperature = relationship("DBTemperature", back_populates="city")
