"""Unit tests for db module - basic smoke tests."""

import pytest
from unittest.mock import patch, MagicMock


def test_db_module_imports():
    """Test that db module can be imported."""
    import db
    assert db is not None


def test_db_notification_module_imports():
    """Test that db_notification module can be imported."""
    import db_notification
    assert db_notification is not None


def test_ensure_db_initialized_mock():
    """Test database initialization with mocks."""
    import db_notification
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
    """Test that first notification can be sent (mocked)."""
    import db_notification
    db_notification._db_initialized = False

    with patch('db_notification.get_session') as mock_session:
        mock_sess = MagicMock()
        mock_session.return_value = mock_sess
        mock_sess.exec.return_value.first.return_value = None

        result, reason = db_notification.can_send_notification_db("test")

        assert result is True
        assert "No test notification sent today" in reason


def test_can_send_notification_db_already_sent():
    """Test that notification is blocked when already sent today."""
    import db_notification
    db_notification._db_initialized = False

    with patch('db_notification.get_session') as mock_session:
        mock_sess = MagicMock()
        mock_session.return_value = mock_sess
        mock_sess.exec.return_value.first.return_value = MagicMock()

        result, reason = db_notification.can_send_notification_db("test")

        assert result is False
        assert "Already sent test notification today" in reason


def test_can_send_notification_db_database_error():
    """Test handling database errors gracefully."""
    import db_notification
    db_notification._db_initialized = False

    with patch('db_notification.get_session') as mock_session:
        mock_session.side_effect = Exception("Database error")

        result, reason = db_notification.can_send_notification_db("test")

        # Should allow notification (fail open)
        assert result is True
        assert "Rate limiting bypassed" in reason
