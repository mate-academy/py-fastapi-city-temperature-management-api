from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base
from app.temperature.models import DBTemperature


class DBCity(Base):
    __tablename__ = "city"

    id = Column(Integer, index=True, primary_key=True)
    city = Column(String(255), unique=True, index=True)
    additional_info = Column(String(510))

    temperature = relationship(DBTemperature, back_populates="cities")
