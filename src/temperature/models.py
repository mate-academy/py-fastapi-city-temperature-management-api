from datetime import datetime

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, ForeignKey, DateTime, Float

from src.database.models import Base

class DbTemperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    city_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("city.id"),
        nullable=False
    )
    date_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    city: Mapped["DbCity"] = relationship(
        "DbCity",
        back_populates="temperatures",
    )