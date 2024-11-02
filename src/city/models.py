from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.db.database import Base
from src.temperature.models import Temperature


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    additional_info = Column(String)

    temperatures = relationship(Temperature, back_populates="city")
