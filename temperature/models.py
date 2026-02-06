from datetime import datetime

from sqlalchemy import (
    Integer,
    ForeignKey,
    DateTime,
    Float
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from database import Base


class DBTemperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id"),
        nullable=False
    )
    date_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
