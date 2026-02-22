"""Unit tests for db_notification module."""

import pytest
from unittest.mock import patch, MagicMock

import db_notification


@pytest.fixture(autouse=True)
def reset_db():
    """Reset the db state between tests."""
    import db
    db._engine = None
    db_notification._db_initialized = False
    yield
    db._engine = None
    db_notification._db_initialized = False


def test_ensure_db_initialized():
    """Test database initialization."""
    db_notification._db_initialized = False

    with patch('db_notification.init_db') as mock_init, \
         patch('db_notification.seed_sources') as mock_seed, \
         patch('db_notification.get_session') as mock_session:

        mock_sess = MagicMock()
        mock_session.return_value = mock_sess

        result = db_notification.ensure_db_initialized()

        assert result is True
        mock_init.assert_called_once()
        mock_seed.assert_called_once()


def test_can_send_notification_db_first_notification():
    """Test that first notification can be sent."""
    db_notification._db_initialized = False

    with patch('db_notification.get_session') as mock_session:
        mock_sess = MagicMock()
        mock_session.return_value = mock_sess

        # Mock no previous notification
        mock_sess.exec.return_value.first.return_value = None

        result, reason = db_notification.can_send_notification_db("test")

        # Should allow notification
        assert result is True
        assert "No test notification sent today" in reason


def test_can_send_notification_db_already_sent():
    """Test that notification is blocked when already sent today."""
    db_notification._db_initialized = False

    with patch('db_notification.get_session') as mock_session:
        mock_sess = MagicMock()
        mock_session.return_value = mock_sess

        # Mock previous notification exists
        mock_sess.exec.return_value.first.return_value = MagicMock()

        result, reason = db_notification.can_send_notification_db("test")

        # Should block notification
        assert result is False
        assert "Already sent test notification today" in reason


def test_can_send_notification_db_database_error():
    """Test handling database errors gracefully."""
    db_notification._db_initialized = False

    with patch('db_notification.get_session') as mock_session:
        mock_session.side_effect = Exception("Database error")

        result, reason = db_notification.can_send_notification_db("test")

        # Should allow notification (fail open)
        assert result is True
        assert "Rate limiting bypassed" in reason


def test_record_notification_db_unavailable():
    """Test recording when database unavailable."""
    db_notification._db_initialized = False

    with patch('db_notification.ensure_db_initialized', return_value=False):
        result = db_notification.record_notification_db("test", "Test message")

        # Should return False
        assert result is False


def test_can_send_notification_db_with_alert_type():
    """Test checking with specific alert type."""
    db_notification._db_initialized = False

    with patch('db_notification.get_session') as mock_session:
        mock_sess = MagicMock()
        mock_session.return_value = mock_sess

        # Mock no previous notification for this alert type
        mock_sess.exec.return_value.first.return_value = None

        result, reason = db_notification.can_send_notification_db("aqi", "current_aqi")

        assert result is True
        # Should pass the alert_type to the query
        mock_sess.exec.assert_called()
