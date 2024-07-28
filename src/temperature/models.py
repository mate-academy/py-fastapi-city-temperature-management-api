from __future__ import annotations

import datetime
from sqlalchemy.orm import mapped_column
from sqlalchemy import DateTime, ForeignKey, Float

from src.database import Base


class Temperature(Base):
    __tablename__ = "temperature"
    city_id = mapped_column(ForeignKey("city.id", ondelete="CASCADE"))
    datetime = mapped_column(DateTime, default=datetime.datetime.now)
    temperature = mapped_column(Float)

    def __repr__(self):
        return f"{self.n} - {self.datetime}"
