from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.sql.sqltypes import Integer, Float

from database.database import Base


class TemperatureModel(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("cities.id", ondelete="CASCADE"), nullable=False
    )
    date_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=func.now(),
        server_default=func.now(),
        nullable=False,
    )
    temperature: Mapped[float] = mapped_column(Float, nullable=False)

    city = relationship("CityModel", back_populates="temperatures")
