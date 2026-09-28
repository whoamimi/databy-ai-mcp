from datetime import datetime, timezone
from pathlib import Path
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from .types import BusinessDomain, CleanState


class SessionForm(BaseModel):
    business_domain: BusinessDomain = Field(
        description="Select the business domain that best matches your case."
    )
    objective: str = Field(
        min_length=1,
        description="What are you using this dataset for?",
    )
    clean_state: CleanState = Field(
        default=CleanState.CLEAN,
        description="Select how messy your dataset is.",
    )


class DatasetFile(BaseModel):
    file_id: UUID = Field(default_factory=uuid4)
    filename: str
    content_type: str | None = None
    size_bytes: int | None = None
    path: Path | None = None
    uploaded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DatabySession(BaseModel):
    session_id: UUID = Field(default_factory=uuid4)
    user_id: UUID = Field(default_factory=uuid4)

    metadata: SessionForm
    files: list[DatasetFile] = Field(default_factory=list)

    status: Literal[
        "created",
        "waiting_for_file",
        "ready",
        "processing",
        "completed",
        "failed",
    ] = "created"

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def is_ready(self) -> bool:
        return bool(self.files) and bool(self.metadata.objective.strip())


# Returned Object:
#
# session = DatabySession(
#     metadata=SessionForm(
#         business_domain=BusinessDomain.TRANSACTIONS,
#         objective="Clean transaction data",
#         clean_state=CleanState.MESS,
#     ),
#     files=[
#         DatasetFile(
#             filename="transactions.csv",
#             content_type="text/csv",
#             size_bytes=125_000,
#             path=Path("data/transactions.csv"),
#         )
#     ],
#     status="ready",
# )
