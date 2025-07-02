from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Temperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    city_id: Mapped[int] = mapped_column(
        ForeignKey("city.id", ondelete="CASCADE"), nullable=False
    )
    date_time: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now
    )
    temperature: Mapped[float] = mapped_column(nullable=False)

    city = relationship(
        "City", back_populates="temperatures", passive_deletes=True
    )

    def __repr__(self):
        return f"<Temperature: {self.temperature}>"
