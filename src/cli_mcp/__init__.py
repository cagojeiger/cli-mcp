"""cli-mcp: A modern Python CLI tool for MCP (Model Context Protocol) server management."""

try:
    from importlib.metadata import version

    __version__ = version("cli-mcp")
except Exception:
    __version__ = "dev"
