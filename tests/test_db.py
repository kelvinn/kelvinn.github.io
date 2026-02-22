"""Unit tests for db module."""

import pytest
from datetime import date, datetime

from db import (
    NotificationSource,
    NotificationHistory,
    seed_sources,
    get_or_create_source,
    check_notification_sent_today,
    record_notification,
    get_session,
    _get_engine,
    init_db,
)


@pytest.fixture
def session():
    """Create a session for testing."""
    import db as db_module
    db_module._engine = None

    from sqlmodel import Session
    engine = _get_engine()
    # Create tables
    init_db()
    sess = Session(engine)
    yield sess
    sess.close()
    # Clean up engine
    db_module._engine = None


def test_notification_source_creation(session):
    """Test creating a notification source."""
    source = NotificationSource(name="test_source", description="Test description")
    session.add(source)
    session.commit()

    result = session.get(NotificationSource, source.id)
    assert result is not None
    assert result.name == "test_source"


def test_notification_history_creation(session):
    """Test creating a notification history entry."""
    source = NotificationSource(name="aqi")
    session.add(source)
    session.commit()

    history = NotificationHistory(
        source_id=source.id,
        notification_date=date.today(),
        notification_time=datetime.now(),
        message="Test message",
        alert_type="test_alert"
    )
    session.add(history)
    session.commit()

    result = session.get(NotificationHistory, history.id)
    assert result is not None
    assert result.message == "Test message"


def test_get_or_create_source_new(session):
    """Test creating a new source."""
    result = get_or_create_source(session, "new_source")
    assert result is not None
    assert result.name == "new_source"


def test_get_session():
    """Test getting a session."""
    import db
    db._engine = None

    session = get_session()
    assert session is not None
    from sqlmodel import Session as SQLSession
    assert isinstance(session, SQLSession)
    session.close()
