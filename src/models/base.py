from sqlalchemy.orm import DeclarativeBase, InstrumentedAttribute, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)

    @classmethod
    def default_order_by(cls) -> InstrumentedAttribute[int]:
        return cls.id
