"""Tests for __init__ module."""

import sys
from unittest.mock import patch


class TestInit:
    """Test __init__ module functionality."""

    def test_version_fallback(self):
        """Test version fallback when package is not installed."""
        # Mock importlib.metadata.version to raise an exception
        with patch("importlib.metadata.version") as mock_version:
            mock_version.side_effect = Exception("Package not found")

            # Remove the module from sys.modules to force reimport
            if "mcpcli" in sys.modules:
                del sys.modules["mcpcli"]

            # Import the module
            import mcpcli

            # Check that version falls back to "dev"
            assert mcpcli.__version__ == "dev"
