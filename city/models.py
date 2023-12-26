from sqlalchemy.orm import relationship

from database import Base
from sqlalchemy import Column, Integer, String


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    additional_info = Column(String(900), nullable=True)
    temperature = relationship("Temperature", back_populates="city")
