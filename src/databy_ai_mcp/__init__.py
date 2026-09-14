# /Users/mimiphan/mimeus-app/databy-ai/databy-ai-mcp/src/databy_ai_mcp/__init__.py
#
# ------------------------------------------------------------------------------
# Last Modified:	Wednesday, 26th August 2026 9:59:24 pm
# Created Date:	Wednesday, 26th Aug 2026 9:49:02 pm
# Copyright (c) 2026 Mimi P. (https://github.com/whoamimi)


def main() -> None:
    from .server import mcp

    return mcp.run()
