import datetime

from sqlalchemy import ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database import Base
from city.models import DBCity


class DBTemperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    date_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    temperature: Mapped[float] = mapped_column(Float, nullable=False)

    city: Mapped["DBCity"] = relationship("DBCity", back_populates="temperatures")
