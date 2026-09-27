# src/databy_ai_mcp/ui/schemas.py
######
#                     Databy AI MCP
#                          │
#              ┌───────────┴───────────┐
#              │                       │
#        input_metadata           input_file
#              │                       │
#        Session Form             File Upload
#              │                       │
#        ┌─────┴─────┐           dataset file
#        │     │     │                 │
#     domain  goal  state              │
#              │                       │
#              └───────────┬───────────┘
#                          │
#                    Databy workflow
#                          │
#                 cleaning / analysis
######

from uuid import UUID, uuid4
from typing import Literal
from pydantic import BaseModel, Field


class SessionForm(BaseModel):
    """Databy Client Entry Point

     Start Session
    │
    ├── SessionForm
    │     ├── business_domain
    │     ├── objective
    │     └── clean_state
    │
    └── FileUpload
          └── dataset
                │
                ▼
         Databy Session
    """

    session_id: UUID | str = Field(
        description="User Session ID", init=False, repr=True, default=uuid4
    )
    user_id: UUID | str = Field(
        description="User ID", init=False, repr=True, default=uuid4
    )
    business_domain: Literal[
        "Chat History",
        "B2C/B2B Transactions",
        "Logistic Dataset",
        "Time Series",
        "Sensory Dataset",
        "User Event",
    ] = Field(
        description="Select the Business domain best matches your case.",
        json_schema_extra={"ui": {"type": "select", "default": True}},
    )
    objective: str = Field(
        description="What are you using this dataset for?",
        json_schema_extra={
            "ui": {
                "type": "text",
            }
        },
    )
    clean_state: Literal["mess", "moderate", "clean"] = Field(
        default="clean",
        description="Select how messy your dataset",
        json_schema_extra={"ui": {"type": "select", "default": False}},
    )


def submit_input(user_input: SessionForm) -> str:
    """TODO:
    - Add Checks
    - Navigate to file upload method
    """
    return user_input.model_dump_json()


class DatabySession(BaseModel):
    metadata: SessionForm
    files: list[str] = Field(default_factory=list)
