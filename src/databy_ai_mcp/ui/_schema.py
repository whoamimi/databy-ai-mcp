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

from typing import Literal
from uuid import UUID, uuid4

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
        description="User Session ID", init=False, repr=True, default_factory=uuid4
    )
    user_id: UUID | str = Field(
        description="User ID", init=False, repr=True, default_factory=uuid4
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


# DatabySessionApp = Form.from_model(DatabySession)

# DatabySessionApp = [
#     Form.from_model(FormInput),
#     FileUpload(
#         name="Upload File",
#         max_file_size=10 * 1024 * 1024,
#         title="File Upload",
#         description=str(
#             "Drop files to upload them to the server. "
#             "The model can then read and analyze them "
#             "without using the context window."
#         ),
#         drop_label="Drop files here. Acceptable filetype extensions: csv, xlsx, parquet, pdf, HTML, img/jpeg.",
#     ),
# ]

# databy_form = FormInput(
#     model=SessionForm,
#     name="Session Form",
#     title="Start Session",
#     submit_text="Submit",
#     on_submit=submit_input,
# )

# databy_file_upload = FileUpload(
#     name="Upload File",
#     max_file_size=10 * 1024 * 1024,
#     title="File Upload",
#     description=(
#         "Drop files to upload them to the server. "
#         "The model can then read and analyze them "
#         "without using the context window."
#     ),
#     drop_label=(
#         "Drop files here. Acceptable filetype extensions: "
#         "csv, xlsx, parquet, pdf, HTML, img/jpeg."
#     ),
# )

# DatabySessionApp = [
#     Form.from_model(databy_form),
#     databy_file_upload,
# ]

# Expected Object:
#
# DatabySession(
#     metadata=SessionForm(
#         session_id=...,
#         user_id=...,
#         business_domain="B2C/B2B Transactions",
#         objective="Clean transaction data",
#         clean_state="mess",
#     ),
#     files=[
#         "transactions.csv",
#     ],
# )


# databy_forms: list[FormInput] = [
#     FormInput(
#         model=SessionForm,  # Required: the Pydantic model
#         name="Session Form",  # App name (default: model name)
#         title="Start Session",  # Card heading (default: model name)
#         # tool_name="collect_sessionform",        # Tool name (default: collect_{model})
#         submit_text="Submit",  # Button label (default: "Submit")
#         on_submit=submit_input,  # Optional callback
#     )
# ]

# databy_file_inputs: list = [
#     FileUpload(
#         name="Upload File",
#         description="Manually upload your dataset to clean.",
#         drop_label="Drop files here. Acceptable filetype extensions: csv, xlsx, parquet, pdf, HTML, img/jpeg.",
#     )
#     # LocalUploadDataset(
#     #     name="Upload Dataset",  # App name (used in tool routing)
#     #     max_file_size=10 * 1024 * 1024,  # 10 MB default, enforced server-side
#     #     title="File Upload",  # Heading shown in the UI
#     #     description="Drop files to...",  # Description text below the heading
#     #     drop_label="Drop files here",  # Label inside the drop zone
#     # )
# ]
