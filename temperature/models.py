from datetime import datetime
from sqlalchemy import (
    Integer,
    Float,
    ForeignKey,
    func,
    DateTime,
)
from sqlalchemy.orm import (
    mapped_column,
    Mapped,
    relationship
)

from db import Base


class Temperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    temperature: Mapped[float] = mapped_column(Float(2))
    city: Mapped["City"] = relationship(back_populates="temperatures") # noqa
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"))
    date_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
