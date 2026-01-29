
from sqlalchemy import ForeignKey, Float, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.base import Base


class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(primary_key=True)
    temperature: Mapped[float] = mapped_column(Float)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    date_time: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
    city: Mapped["City"] = relationship(
        "City",
                 back_populates="temperatures",
                 lazy="selectin"
    )
