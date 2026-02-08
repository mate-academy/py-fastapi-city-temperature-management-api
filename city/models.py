from database import Base

from sqlalchemy.orm import Mapped, mapped_column


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    additional_info: Mapped[str | None]