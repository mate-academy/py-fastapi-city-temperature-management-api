import datetime


from sqlalchemy import DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


from database import Base
import typing


if typing.TYPE_CHECKING:
  from city_crud_api.models import DBCity


class DBTemperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"))
    city: Mapped["DBCity"] = relationship(back_populates="temperatures")
    date_time: Mapped[datetime.datetime] = mapped_column(
            DateTime(timezone=True),
            server_default=func.now()
    )
    temperature: Mapped[float] = mapped_column()
