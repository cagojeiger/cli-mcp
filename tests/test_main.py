"""Tests for __main__ module."""

import subprocess
import sys


class TestMain:
    """Test __main__ module execution."""

    def test_module_execution(self):
        """Test running the module with python -m."""
        result = subprocess.run(
            [sys.executable, "-m", "cli_mcp", "--version"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "cli-mcp version:" in result.stdout
