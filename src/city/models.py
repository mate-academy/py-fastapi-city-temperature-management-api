from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String
from src.database.models import Base


class DbCity(Base):
    __tablename__ = "city"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    additional_info: Mapped[str] = mapped_column(
        String(500), unique=False, nullable=True
    )
    temperatures: Mapped[list["DbTemperature"]] = relationship(
        "DbTemperature", back_populates="city", cascade="all, delete-orphan"
    )
