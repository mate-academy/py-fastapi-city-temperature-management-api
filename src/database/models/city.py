from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String

from database.models.base import Base


class CityModel(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    additional_info: Mapped[str] = mapped_column(String(255), nullable=False)

    temperatures: Mapped[list["TemperatureModel"]] = relationship(
        "TemperatureModel",
        back_populates="city",
        cascade="all, delete-orphan"
    )
