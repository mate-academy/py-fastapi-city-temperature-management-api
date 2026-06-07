import datetime
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from databese import Base


class DBTemperature(Base):
    __tablename__ = "temperature"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date_time: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )
    temperature: Mapped[float]
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"))
    city: Mapped["DBCity"] = relationship(back_populates="temperatures")
