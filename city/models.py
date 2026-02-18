from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base


class City(Base):
    __tablename__ = "city"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    additional_info: Mapped[str] = mapped_column(String(511))

    temperatures = relationship("Temperature", back_populates="city")
