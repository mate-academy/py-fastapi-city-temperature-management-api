from typing import List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.temperature_app import DBTemperature


class DBCity(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    additional_info: Mapped[str] = mapped_column(String, nullable=True)
    temperatures: Mapped[List["DBTemperature"]] = relationship(
        back_populates="city",
        cascade="all, delete-orphan",
    )