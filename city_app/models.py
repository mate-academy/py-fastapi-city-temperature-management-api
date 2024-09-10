from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from database import Base
from temperature_app import models


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    additional_info = Column(String(255), nullable=False)
    temperatures = relationship(models.Temperature, back_populates="city")

    def __repr__(self):
        return self.name
