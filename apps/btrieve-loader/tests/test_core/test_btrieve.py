"""
Tests for core btrieve module.
"""

from unittest.mock import MagicMock, patch

import pytest


class TestBtrieveClientManager:
    """Tests for BtrieveClientManager singleton."""

    def test_singleton_pattern(self):
        """Test that BtrieveClientManager is a singleton."""
        from src.core.btrieve import BtrieveClientManager

        manager1 = BtrieveClientManager()
        manager2 = BtrieveClientManager()

        assert manager1 is manager2

    def test_initialization(self):
        """Test manager initializes correctly."""
        from src.core.btrieve import BtrieveClientManager

        # Create fresh instance for testing
        BtrieveClientManager._instance = None
        manager = BtrieveClientManager()

        assert manager._initialized is True
        assert manager._client is None
        assert manager._open_files == {}

    @patch("src.core.btrieve.BtrieveClient")
    def test_client_property_creates_client(self, mock_client_class):
        """Test client property creates BtrieveClient on first access."""
        from src.core.btrieve import BtrieveClientManager

        # Reset singleton
        BtrieveClientManager._instance = None
        manager = BtrieveClientManager()

        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        client = manager.client

        mock_client_class.assert_called_once()
        assert client is mock_client

    @patch("src.core.btrieve.BtrieveClient")
    def test_client_property_returns_cached(self, mock_client_class):
        """Test client property returns cached instance."""
        from src.core.btrieve import BtrieveClientManager

        # Reset singleton
        BtrieveClientManager._instance = None
        manager = BtrieveClientManager()

        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        client1 = manager.client
        client2 = manager.client

        # Should only create once
        mock_client_class.assert_called_once()
        assert client1 is client2

    @patch("src.core.btrieve.BtrieveClient")
    def test_open_table_success(self, mock_client_class):
        """Test open_table opens and caches table."""
        from src.core.btrieve import BtrieveClientManager

        # Reset singleton
        BtrieveClientManager._instance = None
        manager = BtrieveClientManager()

        mock_client = MagicMock()
        mock_client.STATUS_SUCCESS = 0
        mock_client.open_file.return_value = (0, b"position_block_data")
        mock_client_class.return_value = mock_client

        pos_block = manager.open_table("gscat")

        assert pos_block == b"position_block_data"
        assert "gscat" in manager._open_files
        mock_client.open_file.assert_called_once()

    @patch("src.core.btrieve.BtrieveClient")
    def test_open_table_returns_cached(self, mock_client_class):
        """Test open_table returns cached position block."""
        from src.core.btrieve import BtrieveClientManager

        # Reset singleton
        BtrieveClientManager._instance = None
        manager = BtrieveClientManager()

        mock_client = MagicMock()
        mock_client.STATUS_SUCCESS = 0
        mock_client.open_file.return_value = (0, b"position_block")
        mock_client_class.return_value = mock_client

        pos1 = manager.open_table("gscat")
        pos2 = manager.open_table("gscat")

        # Should only open once
        mock_client.open_file.assert_called_once()
        assert pos1 == pos2

    @patch("src.core.btrieve.BtrieveClient")
    def test_open_table_failure(self, mock_client_class):
        """Test open_table raises on failure."""
        from src.core.btrieve import BtrieveClientManager

        # Reset singleton
        BtrieveClientManager._instance = None
        manager = BtrieveClientManager()

        mock_client = MagicMock()
        mock_client.STATUS_SUCCESS = 0
        mock_client.open_file.return_value = (12, None)  # Status 12 = file not found
        mock_client.get_status_message.return_value = "File not found"
        mock_client_class.return_value = mock_client

        with pytest.raises(RuntimeError, match="Failed to open"):
            manager.open_table("nonexistent")

    @patch("src.core.btrieve.BtrieveClient")
    def test_close_table(self, mock_client_class):
        """Test close_table closes and removes from cache."""
        from src.core.btrieve import BtrieveClientManager

        # Reset singleton
        BtrieveClientManager._instance = None
        manager = BtrieveClientManager()

        mock_client = MagicMock()
        mock_client.STATUS_SUCCESS = 0
        mock_client.open_file.return_value = (0, b"position_block")
        mock_client_class.return_value = mock_client

        manager.open_table("gscat")
        assert "gscat" in manager._open_files

        manager.close_table("gscat")

        assert "gscat" not in manager._open_files
        mock_client.close_file.assert_called_once_with(b"position_block")

    @patch("src.core.btrieve.BtrieveClient")
    def test_close_all(self, mock_client_class):
        """Test close_all closes all tables."""
        from src.core.btrieve import BtrieveClientManager

        # Reset singleton
        BtrieveClientManager._instance = None
        manager = BtrieveClientManager()

        mock_client = MagicMock()
        mock_client.STATUS_SUCCESS = 0
        mock_client.open_file.side_effect = [
            (0, b"pos1"),
            (0, b"pos2"),
        ]
        mock_client_class.return_value = mock_client

        manager.open_table("gscat")
        manager.open_table("pab")
        assert len(manager._open_files) == 2

        manager.close_all()

        assert len(manager._open_files) == 0
        assert mock_client.close_file.call_count == 2

    @patch("src.core.btrieve.BtrieveClient")
    def test_table_session_context_manager(self, mock_client_class):
        """Test table_session context manager."""
        from src.core.btrieve import BtrieveClientManager

        # Reset singleton
        BtrieveClientManager._instance = None
        manager = BtrieveClientManager()

        mock_client = MagicMock()
        mock_client.STATUS_SUCCESS = 0
        mock_client.open_file.return_value = (0, b"position_block")
        mock_client_class.return_value = mock_client

        with manager.table_session("gscat") as pos_block:
            assert pos_block == b"position_block"
            assert "gscat" in manager._open_files

        # Connection stays open for reuse
        assert "gscat" in manager._open_files


class TestBtrieveModuleFunctions:
    """Tests for module-level functions."""

    def test_get_btrieve_client(self):
        """Test get_btrieve_client returns manager."""
        from src.core import btrieve
        from src.core.btrieve import BtrieveClientManager, get_btrieve_client

        # Reset global
        btrieve._manager = None

        manager = get_btrieve_client()

        assert isinstance(manager, BtrieveClientManager)

    def test_get_btrieve_client_returns_same_instance(self):
        """Test get_btrieve_client returns same instance."""
        from src.core import btrieve
        from src.core.btrieve import get_btrieve_client

        # Reset global
        btrieve._manager = None

        manager1 = get_btrieve_client()
        manager2 = get_btrieve_client()

        assert manager1 is manager2

    def test_get_btrieve_manager_alias(self):
        """Test get_btrieve_manager is alias for get_btrieve_client."""
        from src.core import btrieve
        from src.core.btrieve import get_btrieve_client, get_btrieve_manager

        # Reset global
        btrieve._manager = None

        manager1 = get_btrieve_client()
        manager2 = get_btrieve_manager()

        assert manager1 is manager2
