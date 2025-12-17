from datetime import datetime, timezone

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, func

from settings import Base


class Temperature(Base):
    __tablename__ = "temperature"
    id = Column(Integer, primary_key=True)
    city_id = Column(
        Integer,
        ForeignKey("city.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    date_time = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    value = Column(Float, nullable=False)
