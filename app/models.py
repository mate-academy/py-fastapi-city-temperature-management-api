from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    additional_info = Column(String)
    temperatures = relationship(
        "Temperature",
        back_populates="city",
        cascade="all, delete-orphan"  # ORM directive telling SQLAlchemy how to handle related objects in Python during session operatios
    )


class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime, nullable=False)
    temperature = Column(Float, nullable=False)
    city_id = Column(
        Integer,
        ForeignKey(
            "cities.id",
            ondelete="CASCADE",  # Database-enforced cascade behavior (a part of the DDL)
            onupdate="CASCADE"
        ),
        nullable=False
    )
    city = relationship("City", back_populates="temperatures")
