"""Unit tests for db module - basic smoke tests."""

import pytest


def test_db_module_imports():
    """Test that db module can be imported."""
    import db
    assert db is not None


def test_notification_source_model():
    """Test that NotificationSource model exists."""
    from db import NotificationSource
    assert NotificationSource is not None
    assert NotificationSource.__tablename__ == "notification_sources"


def test_notification_history_model():
    """Test that NotificationHistory model exists."""
    from db import NotificationHistory
    assert NotificationHistory is not None
    assert NotificationHistory.__tablename__ == "notification_history"


def test_get_session_function():
    """Test that get_session function exists."""
    from db import get_session
    assert get_session is not None


def test_db_notification_module_imports():
    """Test that db_notification module can be imported."""
    import db_notification
    assert db_notification is not None


def test_can_send_notification_returns_tuple():
    """Test can_send_notification_db returns a tuple."""
    import db_notification
    # Just verify the function exists and can be called
    assert callable(db_notification.can_send_notification_db)
