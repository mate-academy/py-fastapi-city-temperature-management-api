from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String)
    additional_info = Column(String)

    temperatures = relationship("Temperature", back_populates="city")

