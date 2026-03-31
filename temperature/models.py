from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, func, DateTime

from database import Base


class DBTemperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id", ondelete="CASCADE"))
    date_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    temperature: Mapped[float] = mapped_column()

    city: Mapped["DBCity"] = relationship(
        back_populates="temperatures",
    )
