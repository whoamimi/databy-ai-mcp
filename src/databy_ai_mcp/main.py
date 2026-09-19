# src/databy_ai_mcp/main.py


def main() -> None:
    """App's entry point"""

    from .server import mcp

    return mcp.run()
