from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base


class DBCity(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, unique=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    additional_info: Mapped[str] = mapped_column(String(511), nullable=True)

    temperatures = relationship("DBTemperature", back_populates="city")
