from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class CityModel(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    additional_info: Mapped[str | None] = mapped_column(String, nullable=True)

    temperatures: Mapped[list["TemperatureModel"]] = relationship(
        "TemperatureModel", back_populates="city", cascade="all, delete-orphan"
    )
