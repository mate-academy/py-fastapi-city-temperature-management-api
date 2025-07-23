from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.weatherapi.models.base import Base
from src.weatherapi.models.temperature import Temperature


class City(Base):
    __tablename__ = "city_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), unique=True)
    additional_info: Mapped[str] = mapped_column(String, nullable=True)

    temperatures: Mapped[list["Temperature"]] = relationship(
        "Temperature",
        back_populates="city",
        cascade="all, delete-orphan"
    )
