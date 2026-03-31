from datetime import datetime

from sqlalchemy import func

from src.database import Base
from src.City.models import City
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Float


class Temperature(Base):
    __tablename__ = "temperature"

    city_id: Mapped[int] = mapped_column(ForeignKey('city.id', ondelete="CASCADE"))
    date_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    temperature: Mapped[float] = mapped_column(Float)

    city: Mapped[City] = relationship(back_populates="temperatures")
