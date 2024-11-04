from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    additional_info = Column(String, nullable=True)

    temperatures = relationship("Temperature", back_populates="city")