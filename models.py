from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import String, ForeignKey, Numeric

from datetime import datetime  # тип для Python
from sqlalchemy import DateTime

from database import Base


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255) ,nullable=False)
    additional_info: Mapped[str | None] = mapped_column(String(255), nullable=True)
    temperature: Mapped[list["Temperature"]] = relationship(back_populates="city")

class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(ForeignKey('cities.id', ondelete="CASCADE"), nullable=False)
    date_time: Mapped[datetime] = mapped_column(DateTime)
    temperature: Mapped[float] = mapped_column(Numeric(precision=5, scale=2))
    city: Mapped["City"] = relationship(back_populates="temperature")