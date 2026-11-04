from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cities.models import City
from database import Base


class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date_time: Mapped[datetime] = mapped_column(server_default=func.now())
    temperature: Mapped[float] = mapped_column()
    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id", ondelete="CASCADE")
    )

    city: Mapped["City"] = relationship(back_populates="temperature")
