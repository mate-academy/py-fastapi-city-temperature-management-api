from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class City(Base):
    __tablename__ = "city"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(127), nullable=False)
    additional_info = Column(String(511), nullable=False)
    temperatures = relationship("Temperature", back_populates="city")
