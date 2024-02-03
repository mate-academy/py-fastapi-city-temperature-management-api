import datetime
from _decimal import Decimal

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class TemperatureDB(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(primary_key=True)

    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id", ondelete="CASCADE"))
    date_time: Mapped[datetime.datetime] = mapped_column()
    temperature_indicator: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))

    city = relationship(
        "CityDB",
        back_populates="temperature",
    )
