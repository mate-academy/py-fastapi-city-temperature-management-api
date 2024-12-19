from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from temperature.models import DBTemperature


class DBCity(Base):
    __tablename__ = "City"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), index=True)
    additional_info = relationship(DBTemperature)
