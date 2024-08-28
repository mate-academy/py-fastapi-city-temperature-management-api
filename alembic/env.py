import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine
from alembic import context

from cities.models import *
from temperatures.models import *
from database import engine, Base  # Використовується асинхронний engine з вашого коду

# Alembic Config об'єкт, який надає доступ до значень всередині .ini файлу.
config = context.config

# Інтерпретація конфігураційного файлу для Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Додаємо MetaData вашої моделі сюди для підтримки 'autogenerate'.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Запуск міграцій у 'офлайн' режимі.

    Це налаштовує контекст лише з URL-адресою і без Engine.
    """

    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Запуск міграцій у 'онлайн' режимі.

    У цьому сценарії необхідно створити Engine
    та асоціювати підключення з контекстом.
    """

    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
