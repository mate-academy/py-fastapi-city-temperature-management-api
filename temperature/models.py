from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.engine import Base
from sqlalchemy import ForeignKey, DateTime


class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey(
        "cities.id"
    ),
        nullable=False
    )
    date_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    temperature: Mapped[float] = mapped_column(nullable=False)

    city = relationship("City", back_populates="temperature")
