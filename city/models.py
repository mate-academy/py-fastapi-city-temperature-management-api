from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from db.engine import Base


class City(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    additional_info: Mapped[str | None] = mapped_column(String(255), nullable=True)

    temperatures: Mapped[list["Temperature"]] = relationship(
        "Temperature", back_populates="city"
    )
