import uuid

from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column,
    Mapped,
    declared_attr
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from app.config.settings import settings

class Base(DeclarativeBase):

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        """Relationships не используются в repr(), т.к. могут вести к неожиданным подгрузкам"""
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    
if settings.mode.lower() == "test":
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_PARAMS = {}

DATABASE_URL = settings.postgres_uri


engine = create_async_engine(
    DATABASE_URL,
    **DATABASE_PARAMS,
)  #  echo=True

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)