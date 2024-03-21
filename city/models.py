from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from project_engine.database import Base


class DBCity(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    additional_info = Column(String(1000), nullable=True)
    # reverse relationship with DBTemperature model
    temperatures = relationship("DBTemperature", back_populates="city")
