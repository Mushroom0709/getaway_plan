"""create all 17 tables

Revision ID: 001
Revises:
Create Date: 2026-07-23 22:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- trips ---
    op.create_table(
        "trips",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column(
            "status",
            sa.Enum("planning", "active", "completed", name="tripstatus"),
            nullable=False,
            server_default="planning",
        ),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # --- days ---
    op.create_table(
        "days",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("trip_id", sa.Integer(), nullable=False),
        sa.Column("day_number", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date(), nullable=True),
        sa.Column("title", sa.String(200), nullable=True),
        sa.Column("drive_hours", sa.Numeric(3, 1), nullable=True),
        sa.Column("hotel_city", sa.String(100), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.ForeignKeyConstraint(["trip_id"], ["trips.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # --- spots ---
    op.create_table(
        "spots",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("trip_id", sa.Integer(), nullable=False),
        sa.Column("day_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("lng", sa.Numeric(10, 6), nullable=False),
        sa.Column("lat", sa.Numeric(10, 6), nullable=False),
        sa.Column(
            "category",
            sa.Enum(
                "airport", "highspeed_rail", "train", "scenic",
                "photo", "hotel", "restaurant", "other",
                name="spotcategory",
            ),
            nullable=False,
            server_default="other",
        ),
        sa.Column("is_nav_point", sa.Boolean(), server_default="0"),
        sa.Column("nav_order", sa.Integer(), nullable=True),
        sa.Column("arrival_time", sa.Time(), nullable=True),
        sa.Column("description", sa.String(500), nullable=True),
        sa.Column("intro", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["trip_id"], ["trips.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["day_id"], ["days.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    # --- hotels ---
    op.create_table(
        "hotels",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("trip_id", sa.Integer(), nullable=False),
        sa.Column("spot_id", sa.Integer(), nullable=True),
        sa.Column("city", sa.String(100), nullable=False),
        sa.Column("name", sa.String(300), nullable=False),
        sa.Column("brand", sa.String(200), nullable=True),
        sa.Column("rating", sa.Numeric(2, 1), nullable=True),
        sa.Column("opened_year", sa.Integer(), nullable=True),
        sa.Column("price_per_room", sa.Numeric(10, 2), nullable=True),
        sa.Column("room_type", sa.String(200), nullable=True),
        sa.Column("features", sa.JSON(), nullable=True),
        sa.Column("check_in_date", sa.Date(), nullable=True),
        sa.Column("check_out_date", sa.Date(), nullable=True),
        sa.Column("lng", sa.Numeric(10, 6), nullable=True),
        sa.Column("lat", sa.Numeric(10, 6), nullable=True),
        sa.Column("phone", sa.String(50), nullable=True),
        sa.Column("cover_image", sa.String(500), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["trip_id"], ["trips.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["spot_id"], ["spots.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    # --- restaurants ---
    op.create_table(
        "restaurants",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("trip_id", sa.Integer(), nullable=False),
        sa.Column("spot_id", sa.Integer(), nullable=True),
        sa.Column("city", sa.String(100), nullable=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("address", sa.String(300), nullable=True),
        sa.Column("lng", sa.Numeric(10, 6), nullable=True),
        sa.Column("lat", sa.Numeric(10, 6), nullable=True),
        sa.Column("rating", sa.Numeric(2, 1), nullable=True),
        sa.Column("avg_price", sa.Numeric(10, 2), nullable=True),
        sa.Column("cuisine", sa.String(100), nullable=True),
        sa.Column("phone", sa.String(50), nullable=True),
        sa.Column("opening_hours", sa.String(200), nullable=True),
        sa.Column("maps_url", sa.String(500), nullable=True),
        sa.Column("cover_image", sa.String(500), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["trip_id"], ["trips.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["spot_id"], ["spots.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    # --- dishes ---
    op.create_table(
        "dishes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("restaurant_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("price", sa.Numeric(10, 2), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("image", sa.String(500), nullable=True),
        sa.Column("is_signature", sa.Boolean(), server_default="0"),
        sa.ForeignKeyConstraint(["restaurant_id"], ["restaurants.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # --- daily_meals ---
    op.create_table(
        "daily_meals",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("day_id", sa.Integer(), nullable=False),
        sa.Column("restaurant_id", sa.Integer(), nullable=False),
        sa.Column(
            "meal_type",
            sa.Enum("breakfast", "lunch", "dinner", "snack", name="mealtype"),
            nullable=False,
        ),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["day_id"], ["days.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["restaurant_id"], ["restaurants.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # --- attractions ---
    op.create_table(
        "attractions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("spot_id", sa.Integer(), nullable=False),
        sa.Column("ticket_price", sa.String(100), nullable=True),
        sa.Column("opening_hours", sa.String(200), nullable=True),
        sa.Column("best_season", sa.String(200), nullable=True),
        sa.Column("best_time_of_day", sa.String(100), nullable=True),
        sa.Column("duration_hours", sa.Numeric(3, 1), nullable=True),
        sa.Column("altitude", sa.Integer(), nullable=True),
        sa.Column("tips", sa.Text(), nullable=True),
        sa.Column("highlights", sa.JSON(), nullable=True),
        sa.Column("must_see", sa.Boolean(), server_default="0"),
        sa.ForeignKeyConstraint(["spot_id"], ["spots.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("spot_id"),
    )

    # --- flights ---
    op.create_table(
        "flights",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("trip_id", sa.Integer(), nullable=False),
        sa.Column("flight_no", sa.String(20), nullable=False),
        sa.Column("airline", sa.String(100), nullable=True),
        sa.Column("departure_city", sa.String(100), nullable=False),
        sa.Column("departure_airport", sa.String(200), nullable=True),
        sa.Column("arrival_city", sa.String(100), nullable=False),
        sa.Column("arrival_airport", sa.String(200), nullable=True),
        sa.Column("departure_time", sa.DateTime(), nullable=False),
        sa.Column("arrival_time", sa.DateTime(), nullable=False),
        sa.Column("duration_min", sa.Integer(), nullable=True),
        sa.Column("price", sa.Numeric(10, 2), nullable=True),
        sa.Column("seat_class", sa.String(50), nullable=True),
        sa.Column("booking_link", sa.String(500), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["trip_id"], ["trips.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # --- highspeed_rails ---
    op.create_table(
        "highspeed_rails",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("trip_id", sa.Integer(), nullable=False),
        sa.Column("train_no", sa.String(20), nullable=False),
        sa.Column("departure_city", sa.String(100), nullable=False),
        sa.Column("departure_station", sa.String(200), nullable=False),
        sa.Column("arrival_city", sa.String(100), nullable=False),
        sa.Column("arrival_station", sa.String(200), nullable=False),
        sa.Column("departure_time", sa.DateTime(), nullable=False),
        sa.Column("arrival_time", sa.DateTime(), nullable=False),
        sa.Column("duration_min", sa.Integer(), nullable=True),
        sa.Column("price", sa.Numeric(10, 2), nullable=True),
        sa.Column("seat_class", sa.String(50), nullable=True),
        sa.Column("booking_link", sa.String(500), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["trip_id"], ["trips.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # --- rental_cars ---
    op.create_table(
        "rental_cars",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("trip_id", sa.Integer(), nullable=False),
        sa.Column("platform", sa.String(100), nullable=True),
        sa.Column("car_name", sa.String(200), nullable=False),
        sa.Column("daily_price", sa.Numeric(10, 2), nullable=True),
        sa.Column("engine", sa.String(100), nullable=True),
        sa.Column("seats", sa.Integer(), nullable=True),
        sa.Column("trunk", sa.String(100), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["trip_id"], ["trips.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # --- route_segments ---
    op.create_table(
        "route_segments",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("trip_id", sa.Integer(), nullable=False),
        sa.Column("from_spot_id", sa.Integer(), nullable=True),
        sa.Column("to_spot_id", sa.Integer(), nullable=True),
        sa.Column("distance_km", sa.Numeric(8, 2), nullable=True),
        sa.Column("duration_min", sa.Integer(), nullable=True),
        sa.Column("polyline", sa.Text(), nullable=True),
        sa.Column("color", sa.String(20), nullable=True),
        sa.Column("day_number", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["trip_id"], ["trips.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["from_spot_id"], ["spots.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["to_spot_id"], ["spots.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    # --- budget_items ---
    op.create_table(
        "budget_items",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("trip_id", sa.Integer(), nullable=False),
        sa.Column(
            "category",
            sa.Enum(
                "flight", "hotel", "car", "food", "ticket", "rail", "other",
                name="budgetcategory",
            ),
            nullable=False,
        ),
        sa.Column("item", sa.String(300), nullable=False),
        sa.Column("unit_price", sa.Numeric(10, 2), nullable=True),
        sa.Column("quantity", sa.Integer(), server_default="1"),
        sa.Column("subtotal", sa.Numeric(10, 2), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["trip_id"], ["trips.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # --- weather ---
    op.create_table(
        "weather",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("trip_id", sa.Integer(), nullable=False),
        sa.Column("city", sa.String(100), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("high_temp", sa.String(20), nullable=True),
        sa.Column("low_temp", sa.String(20), nullable=True),
        sa.Column("weather_desc", sa.String(200), nullable=True),
        sa.Column("advice", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["trip_id"], ["trips.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # --- social_notes ---
    op.create_table(
        "social_notes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("spot_id", sa.Integer(), nullable=False),
        sa.Column(
            "platform",
            sa.Enum("xiaohongshu", "douyin", name="platform"),
            nullable=False,
        ),
        sa.Column("note_id", sa.String(100), nullable=False),
        sa.Column("title", sa.String(500), nullable=True),
        sa.Column("author", sa.String(200), nullable=True),
        sa.Column("author_id", sa.String(100), nullable=True),
        sa.Column("likes", sa.Integer(), server_default="0"),
        sa.Column("comments", sa.Integer(), server_default="0"),
        sa.Column("shares", sa.Integer(), server_default="0"),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("xsec_token", sa.String(200), nullable=True),
        sa.Column("source_url", sa.String(500), nullable=True),
        sa.Column("note_type", sa.String(50), nullable=True),
        sa.Column("fetched_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["spot_id"], ["spots.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # --- social_images ---
    op.create_table(
        "social_images",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("note_id", sa.Integer(), nullable=False),
        sa.Column("url", sa.String(500), nullable=True),
        sa.Column("url_large", sa.String(500), nullable=True),
        sa.Column("width", sa.Integer(), nullable=True),
        sa.Column("height", sa.Integer(), nullable=True),
        sa.Column("sort_order", sa.Integer(), server_default="0"),
        sa.Column("local_path", sa.String(500), nullable=True),
        sa.ForeignKeyConstraint(["note_id"], ["social_notes.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # --- auth_tokens ---
    op.create_table(
        "auth_tokens",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("device_id", sa.String(200), nullable=False),
        sa.Column("token", sa.String(500), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_auth_tokens_device_id", "auth_tokens", ["device_id"])


def downgrade() -> None:
    op.drop_table("auth_tokens")
    op.drop_table("social_images")
    op.drop_table("social_notes")
    op.drop_table("weather")
    op.drop_table("budget_items")
    op.drop_table("route_segments")
    op.drop_table("rental_cars")
    op.drop_table("highspeed_rails")
    op.drop_table("flights")
    op.drop_table("attractions")
    op.drop_table("daily_meals")
    op.drop_table("dishes")
    op.drop_table("restaurants")
    op.drop_table("hotels")
    op.drop_table("spots")
    op.drop_table("days")
    op.drop_table("trips")
