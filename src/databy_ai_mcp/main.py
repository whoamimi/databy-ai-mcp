# src/databy_ai_mcp/main.py

import uvicorn

from .utils.logging import LOGGING_CONFIG

if __name__ == "__main__":
    uvicorn.run(
        "databy_ai_mcp.server:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING_CONFIG,
    )
