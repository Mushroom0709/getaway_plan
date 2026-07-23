import asyncio
import os
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from app.models.trip import Base
from app.models.day import Day
from app.models.spot import Spot
from app.models.hotel import Hotel
from app.models.restaurant import Restaurant
from app.models.dish import Dish
from app.models.daily_meal import DailyMeal
from app.models.attraction import Attraction
from app.models.flight import Flight
from app.models.highspeed_rail import HighspeedRail
from app.models.rental_car import RentalCar
from app.models.route_segment import RouteSegment
from app.models.budget_item import BudgetItem
from app.models.weather import Weather
from app.models.social_note import SocialNote
from app.models.social_image import SocialImage
from app.models.auth_token import AuthToken

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# Override sqlalchemy.url with DATABASE_URL env var if set
db_url = os.environ.get("DATABASE_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
