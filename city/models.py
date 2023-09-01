from sqlalchemy import Column, Integer, String

from database import Base
from sqlalchemy.orm import relationship
from temperature_api.models import Temperature


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    additional_info = Column(String(255), nullable=True)

    temperatures = relationship(Temperature, back_populates="city")
