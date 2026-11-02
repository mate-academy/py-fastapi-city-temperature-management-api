from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class DBTemperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"))
    date_time: Mapped[datetime]
    temperature: Mapped[float]

    city: Mapped["DBCity"] = relationship(back_populates="temperatures")
