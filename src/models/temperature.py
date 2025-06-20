from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.models.city import CityModel

if TYPE_CHECKING:
    from src.models.city import CityModel


class TemperatureModel(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"), nullable=False)
    date_time: Mapped[datetime] = mapped_column(nullable=False)
    temperature: Mapped[float] = mapped_column(nullable=False)

    # Relationships
    city: Mapped["CityModel"] = relationship("CityModel", back_populates="temperature")
