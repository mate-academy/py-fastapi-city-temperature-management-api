from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float
import datetime

from database import Base


class Temperature(Base):
    __tablename__ = "temperature"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    city_id: int = Column(Integer, ForeignKey("city.id"), nullable=False)
    datetime: datetime = Column(
        DateTime,
        default=datetime.datetime.now(datetime.timezone.utc),
        nullable=False,
    )
    temperature: float = Column(Float, nullable=False)
