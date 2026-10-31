from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base
from temperature.models import Temperature


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    additional_info: Mapped[str] = mapped_column(nullable=True)
    temperature: Mapped[list[Temperature]] = relationship(
        "Temperature", back_populates="city"
    )
