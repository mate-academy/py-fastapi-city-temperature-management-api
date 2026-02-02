from datetime import datetime

from sqlalchemy import func, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from .city import City


class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )

    temperature: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    date_time: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False
    )

    city: Mapped[City] = relationship(
        back_populates="temperatures"
    )
