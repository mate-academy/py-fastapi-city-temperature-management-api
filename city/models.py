from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(55), index=True)
    additional_info = Column(String(255), nullable=True)

    temperatures = relationship("Temperature", back_populates="city")
