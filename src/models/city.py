from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.temperature import TemperatureModel


class CityModel(Base):
    __tablename__ = "city"

    name: Mapped[str] = mapped_column(String(30), unique=True)
    additional_info: Mapped[str] = mapped_column(String(255), nullable=True)

    temperature: Mapped["TemperatureModel"] = relationship("TemperatureModel", back_populates="city")

    def __str__(self):
        return f"{self.name}, {self.additional_info}"
