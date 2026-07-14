from datetime import datetime
from decimal import Decimal
from zoneinfo import ZoneInfo

from sqlalchemy import func, ForeignKey, Numeric, UniqueConstraint, DateTime, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from city_api.models import City
from database import Base


class Temperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    temperature: Mapped[Decimal] = mapped_column(Numeric(4, 2))
    date_time: Mapped[datetime] = mapped_column(DateTime(), server_default=func.now())
    time_zone: Mapped[str] = mapped_column(nullable=False)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id", ondelete="CASCADE"))

    city: Mapped[City] = relationship("City")

    __table_args__ = (
        UniqueConstraint("city_id", "date_time", "time_zone", name="uq_city_datetime"),
    )
