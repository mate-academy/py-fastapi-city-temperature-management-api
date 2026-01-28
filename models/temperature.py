from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Float, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"),
                                         index=True,
                                         nullable=False)

    date_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )
    temperature: Mapped[float] = mapped_column(Float, nullable=False)

    city = relationship("City", back_populates="temperatures")
