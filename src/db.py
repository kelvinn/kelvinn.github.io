"""Database models and configuration for notification history."""

import os
import logging
from datetime import datetime, date
from typing import Optional

from sqlmodel import SQLModel, Field, Session, create_engine, select
from sqlalchemy.pool import StaticPool

logger = logging.getLogger(__name__)

# Database URL from environment - use lazy evaluation to handle tests
def _get_database_url():
    return os.getenv("DATABASE_URL")

# Engine is created lazily
_engine = None

def _get_engine():
    """Get or create the database engine."""
    global _engine
    if _engine is not None:
        return _engine

    database_url = _get_database_url()
    if database_url:
        # Set server_version_info for CockroachDB compatibility
        dialect_options = {}
        if database_url.startswith("postgresql://") or database_url.startswith("postgres://"):
            dialect_options["postgresql"] = {"server_version_info": (15, 1)}
        _engine = create_engine(database_url, pool_pre_ping=True, dialect_options=dialect_options)
    else:
        logger.warning("DATABASE_URL not set, using in-memory SQLite")
        _engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
    return _engine


def get_engine():
    """Get the database engine."""
    return _get_engine()


def init_db():
    """Initialize database tables."""
    SQLModel.metadata.create_all(_get_engine())


class NotificationSource(SQLModel, table=True):
    """Table for notification sources (e.g., 'aqi', 'rain')."""

    __tablename__ = "notification_sources"
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, unique=True, index=True)
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class NotificationHistory(SQLModel, table=True):
    """Table for notification history."""

    __tablename__ = "notification_history"
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    source_id: int = Field(foreign_key="notification_sources.id")
    notification_date: date = Field(index=True)  # The date of the notification
    notification_time: datetime = Field(default_factory=datetime.utcnow)  # Exact time sent
    message: Optional[str] = None  # The notification message
    alert_type: Optional[str] = None  # e.g., "current_aqi", "forecast_risk", "rain_4h", "rain_90m"


def seed_sources(session: Session):
    """Seed the notification sources table with default sources."""
    default_sources = [
        {"name": "aqi", "description": "Air Quality Index notifications for Sydney"},
        {"name": "rain", "description": "Rain probability notifications for Neutral Bay"},
    ]

    for source_data in default_sources:
        # Check if source already exists
        existing = session.exec(
            select(NotificationSource).where(NotificationSource.name == source_data["name"])
        ).first()

        if not existing:
            source = NotificationSource(**source_data)
            session.add(source)

    session.commit()


def get_or_create_source(session: Session, source_name: str) -> Optional[NotificationSource]:
    """Get or create a notification source by name."""
    source = session.exec(
        select(NotificationSource).where(NotificationSource.name == source_name)
    ).first()

    if not source:
        # Try to create it
        source = NotificationSource(name=source_name)
        session.add(source)
        session.commit()
        session.refresh(source)

    return source


def check_notification_sent_today(session: Session, source_name: str, alert_type: Optional[str] = None) -> bool:
    """
    Check if a notification has already been sent today for the given source.

    Args:
        session: Database session
        source_name: The source name (e.g., "aqi", "rain")
        alert_type: Optional specific alert type to check (e.g., "current_aqi", "rain_90m")

    Returns:
        True if notification already sent today, False otherwise
    """
    today = date.today()

    query = select(NotificationHistory).where(
        NotificationHistory.notification_date == today,
        NotificationHistory.source.has(NotificationSource.name == source_name)
    )

    if alert_type:
        query = query.where(NotificationHistory.alert_type == alert_type)

    result = session.exec(query).first()
    return result is not None


def record_notification(
    session: Session,
    source_name: str,
    message: str,
    alert_type: Optional[str] = None
) -> bool:
    """
    Record a notification in the history.

    Args:
        session: Database session
        source_name: The source name (e.g., "aqi", "rain")
        message: The notification message
        alert_type: Optional specific alert type

    Returns:
        True if recorded successfully, False otherwise
    """
    source = get_or_create_source(session, source_name)
    if not source:
        logger.error(f"Failed to get or create source: {source_name}")
        return False

    today = date.today()

    notification = NotificationHistory(
        source_id=source.id,
        notification_date=today,
        notification_time=datetime.utcnow(),
        message=message,
        alert_type=alert_type
    )

    session.add(notification)
    session.commit()

    logger.info(f"Recorded {source_name} notification for {today}")
    return True


def get_session() -> Session:
    """Create and return a new database session."""
    return Session(_get_engine())
