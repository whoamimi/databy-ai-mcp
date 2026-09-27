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

from fastmcp.apps.form import FormInput
from fastmcp.apps.file_upload import FileUpload


class LocalUploadDataset(FileUpload):
    """UserUploadDataset

    User manually uploads or inserts or drops dataset file.

    The LLM sees file_manager, list_files, and read_file. It calls file_manager to show the upload interface, then uses list_files and read_file to work with whatever the user uploaded. store_files is app-only — the UI calls it directly and the LLM never needs to know about it.

    Acceptable file types include:
    - *.csv,
    - *.xlsx,
    - *.html,
    - *.parquet.
    """

    def on_store(self, files, ctx):
        pass

    def on_list(self, ctx):
        pass

    def on_read(self, name, ctx):
        pass


class ConnectOpenSourceDataset(FileUpload):
    """UserUploadDataset

    User connects dataset from Open source environment.
    """

    def on_store(self, files, ctx):
        pass

    def on_list(self, ctx):
        pass

    def on_read(self, name, ctx):
        pass


class ConnectDatabase(FileUpload):
    """UserUploadDataset

    User connects dataset from Open source environment.
    """

    def on_store(self, files, ctx):
        pass

    def on_list(self, ctx):
        pass

    def on_read(self, name, ctx):
        pass


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


from fastmcp.apps import forms

DatabySessionApp = forms.from_model(
    FormInput,
    FileUpload(
        name="Upload File",
        max_file_size=10 * 1024 * 1024,
        title="File Upload",
        description=str(
            "Drop files to upload them to the server. "
            "The model can then read and analyze them "
            "without using the context window."
        ),
        drop_label="Drop files here. Acceptable filetype extensions: csv, xlsx, parquet, pdf, HTML, img/jpeg.",
    ),
)

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
