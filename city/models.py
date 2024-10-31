from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base
from temperature import models


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(127))
    additional_info = Column(String(511))

    temperatures = relationship(models.Temperature, back_populates="city")
