"""Database notification service for rate limiting notifications."""

import logging
from typing import Optional, Tuple

from src.db import (
    get_session,
    check_notification_sent_today,
    record_notification,
    seed_sources,
    init_db,
)

logger = logging.getLogger(__name__)

# Track if DB was initialized
_db_initialized = False


def ensure_db_initialized() -> bool:
    """Initialize the database if needed."""
    global _db_initialized
    if _db_initialized:
        return True

    try:
        init_db()
        # Seed default sources
        session = get_session()
        try:
            seed_sources(session)
        finally:
            session.close()
        _db_initialized = True
        logger.info("Database initialized successfully")
        return True
    except Exception as e:
        logger.warning(f"Failed to initialize database: {e}")
        return False


def can_send_notification_db(source_name: str, alert_type: Optional[str] = None) -> Tuple[bool, str]:
    """
    Check if a notification can be sent based on database rate limiting.

    Args:
        source_name: The source name (e.g., "aqi", "rain")
        alert_type: Optional specific alert type to check

    Returns:
        Tuple of (can_send: bool, reason: str)
    """
    if not ensure_db_initialized():
        return True, "Rate limiting disabled (database unavailable)"

    try:
        session = get_session()
        try:
            already_sent = check_notification_sent_today(session, source_name, alert_type)
            if already_sent:
                return False, f"Already sent {source_name} notification today"
            return True, f"No {source_name} notification sent today"
        finally:
            session.close()
    except Exception as e:
        logger.warning(f"Error checking notification rate limit: {e}")
        return True, "Rate limiting bypassed (database error)"


def record_notification_db(
    source_name: str,
    message: str,
    alert_type: Optional[str] = None
) -> bool:
    """
    Record a notification in the database.

    Args:
        source_name: The source name (e.g., "aqi", "rain")
        message: The notification message
        alert_type: Optional specific alert type

    Returns:
        True if recorded successfully, False otherwise
    """
    if not ensure_db_initialized():
        logger.warning("Cannot record notification: database unavailable")
        return False

    try:
        session = get_session()
        try:
            result = record_notification(session, source_name, message, alert_type)
            return result
        finally:
            session.close()
    except Exception as e:
        logger.warning(f"Error recording notification: {e}")
        return False


def is_database_available() -> bool:
    """Check if the database is available."""
    try:
        if not ensure_db_initialized():
            return False

        session = get_session()
        try:
            # Simple query to test connectivity
            session.execute("SELECT 1")
            return True
        finally:
            session.close()
    except Exception as e:
        logger.warning(f"Database not available: {e}")
        return False
