
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from temperature_api.models import DBTemperature


class DBCity(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    additional_info: Mapped[str] = mapped_column(String(255), nullable=True)
    temperatures: Mapped[list[DBTemperature]] = relationship(back_populates="city")