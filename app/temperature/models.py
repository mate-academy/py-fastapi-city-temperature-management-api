from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String, ForeignKey

from app.database import Base


class Temperature(Base):

    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(
        ForeignKey("city.id", ondelete="CASCADE"),
        nullable=False
    )
    date_time = Column(
        DateTime(),
        nullable=False,
        default=datetime.now()
    )
    temperature = Column(String(255), nullable=False)
