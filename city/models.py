from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from databese import Base


class DBCity(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    additional_info: Mapped[str]

    temperatures: Mapped[list["DBTemperature"]] = relationship(
        "DBTemperature",
        back_populates="city"
    )
