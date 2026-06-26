from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database import Base


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    additional_info: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    temperatures = relationship(
        "Temperature",
        back_populates="city",
        cascade="all, delete-orphan",
    )
    