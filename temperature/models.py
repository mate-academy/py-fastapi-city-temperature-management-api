from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base

class Temperature(Base):
    __tablename__ = "temperature"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"))
    city: Mapped["City"] = relationship(back_populates="temperatures")
    date_time: Mapped[datetime] = mapped_column(nullable=False,
                                                server_default=func.now())
    temperature: Mapped[float] = mapped_column(nullable=False)