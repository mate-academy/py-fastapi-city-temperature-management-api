from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class DBCity(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    additional_info: Mapped[str] = mapped_column(nullable=True)
    temperature: Mapped[list["DBTemperature"]] = relationship(
        back_populates="city",
        cascade="all, delete-orphan",
    )
