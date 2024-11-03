from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.engine import BaseSQLAlchemyModel


class DBCity(BaseSQLAlchemyModel):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(127), nullable=False, unique=True)
    additional_info = Column(String(255))

    temperature = relationship(
        "DBTemperature", back_populates="city", uselist=False
    )


class DBTemperature(BaseSQLAlchemyModel):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Integer, nullable=False)
    date_time = Column(DateTime, server_default=func.now())
    city_id = Column(Integer, ForeignKey("city.id"))

    city = relationship("DBCity", back_populates="temperature")
