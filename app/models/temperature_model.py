from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

from app.models import city_model


class DBTemperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"), nullable=False)
    date_time: Mapped[datetime] = mapped_column(nullable=False)
    temperature: Mapped[float] = mapped_column(nullable=False)

    city: Mapped[city_model.DBCity] = relationship(
        back_populates="temperatures"
    )
