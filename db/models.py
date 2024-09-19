from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from db.database import BaseModel


class City(BaseModel):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    additional_info = Column(String(255), nullable=True)

    temperatures = relationship(
        "Temperature",
        back_populates="city",
        cascade="all,delete-orphan"
    )


class Temperature(BaseModel):
    __tablename__ = "temperatures"
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(
        Integer,
        ForeignKey("cities.id", ondelete="CASCADE"),
        nullable=False
    )
    date_time = Column(DateTime, nullable=False)
    temperature = Column(Float, nullable=False)
    city = relationship(
        City,
        back_populates="temperatures"
    )
