from sqlalchemy import ForeignKey, Integer, Float, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cities.models import Base, City


class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id", ondelete="CASCADE"),
        nullable=False
    )
    date_time: Mapped[DateTime] = mapped_column(
        DateTime,
        default=func.now(),
        nullable=False
    )
    temperature: Mapped[float] = mapped_column(Float, nullable=False)

    city: Mapped["City"] = relationship(back_populates="temperatures")
