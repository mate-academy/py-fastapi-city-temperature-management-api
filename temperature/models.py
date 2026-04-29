from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Temperature(Base):
    __tablename__ = 'temperature'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date_time: Mapped[datetime] = mapped_column(nullable=False)
    temperature: Mapped[float] = mapped_column(nullable=True)
    city_id: Mapped[int] = mapped_column(
        ForeignKey("city.id"), nullable=False
    )
