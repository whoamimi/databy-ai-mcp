# /Users/mimiphan/mimeus-app/databy-ai/databy-ai-mcp/src/databy_ai_mcp/ui/provider.py
#
# ------------------------------------------------------------------------------
# Last Modified:	Wednesday, 26th August 2026 10:27:26 pm
# Created Date:	Wednesday, 26th Aug 2026 10:27:25 pm
# Copyright (c) 2026 Mimi P. (https://github.com/whoamimi)

from fastmcp import FastMCP

from ..logging_config import get_logger

logger = get_logger(__name__)


def databy_resource_providers(mcp: FastMCP):
    """Databy Prefab App Generative or pre-defined UI tools"""

    logger.debug("registering databy resource providers on %s", mcp.name)

    @mcp.resource(
        uri="databy://{user_id}/session/{session_id}",
        name="ApplicationStatus",  # Custom name
        description="Provides the current status of the application.",  # Custom description
        mime_type="application/json",  # Explicit MIME type
        tags={
            "input",
            "init-session",
            "configuration",
            "start",
            "0",
        },  # Categorization tags
        # meta={"version": "2.1", "team": "infrastructure"},
    )
    async def get_current_session(user_id: str, session_id: str):
        """Displays user's most recent and active session config."""

        return f"""
    Session Info:
        UUID: 1234-test-demo
        Input Data:
            - Method: Upload
            - Filetype: CSV
        Metadata:
            - Data filename: Test Demo
            - Upload Method: CSV
            - Objective: Used to train prediction models.
            - Business Domain: Marketing

    """

    @mcp.resource(
        uri="databy://{user_id}/session/{session_id}/data-profile",
        name="DataProfile",  # Custom name
        description="Data Profile Summary",  # Custom description
        mime_type="application/json",  # Explicit MIME type
        tags={"exploratory", "1"},  # Categorization tags
    )
    async def session_data_profile(user_id: str, session_id: str):
        """Displays user's most recent and active session config."""

        return "Data Profile Test!"
