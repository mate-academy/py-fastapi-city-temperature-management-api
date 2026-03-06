from datetime import datetime

from sqlalchemy import ForeignKey, Float, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from city.models import City
from database import Base


class Temperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(
        ForeignKey("city.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    date_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    temperature: Mapped[float] = mapped_column(Float, nullable=False)

    city: Mapped[City] = relationship(back_populates="temperatures")
