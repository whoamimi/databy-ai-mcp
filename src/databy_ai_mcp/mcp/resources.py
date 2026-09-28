# src.databy_ai_mcp.mcp.resources

from fastmcp import FastMCP
from fastmcp.utilities.ui import create_secure_html_response

from ..core.profiler import profile_dataset
from ..utils.logging import get_logger

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

        return """
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
    async def get_session_profiler(user_id: str, session_id: str):
        """Displays user's most recent and active session config."""

        html = profile_dataset(session_id, user_id=user_id)
        return create_secure_html_response(html, status_code=200)
