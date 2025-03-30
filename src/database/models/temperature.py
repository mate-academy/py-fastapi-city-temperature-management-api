from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, DateTime, ForeignKey, func
from datetime import datetime

from database.models.base import Base


class TemperatureModel(Base):
    __tablename__ = "city_temperatures"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey("cities.id", ondelete="CASCADE"))
    date_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        nullable=False
    )
    city: Mapped["CityModel"] = relationship("CityModel", back_populates="temperatures")
