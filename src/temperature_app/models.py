from datetime import datetime

from sqlalchemy import Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.database import Base


class DBTemperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    date_time: Mapped[datetime] = mapped_column(
        DateTime,
    )
    temperature: Mapped[float] = mapped_column(Float)
    city_id: Mapped[int] = mapped_column(ForeignKey(
        "city.id",
        ondelete="CASCADE"
    ))
    city: Mapped["DBCity"] = relationship(back_populates="temperatures")
