
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base

from city.models import DBCity

class DBTemperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"), nullable=False)
    city: Mapped["DBCity"] = relationship(back_populates="temperatures")
    temperature: Mapped[str] = mapped_column(nullable=True)
