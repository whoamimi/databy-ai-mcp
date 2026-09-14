# /Users/mimiphan/mimeus-app/databy-ai/databy-ai-mcp/src/databy_ai_mcp/ui/schemas.py
#
# -----
# Last Modified:	Wednesday, 26th August 2026 10:13:42 pm
# Created Date:	Wednesday, 26th Aug 2026 10:13:41 pm
# Copyright (c) 2026 Mimi P. (https://github.com/whoamimi)

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


class SessionForm(BaseModel):
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
        description="What are u using this for?",
        json_schema_extra={"ui": {"type": "select", "default": True}},
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


databy_forms: list[FormInput] = [
    FormInput(
        model=SessionForm,  # Required: the Pydantic model
        name="Session Form",  # App name (default: model name)
        title="Start Session",  # Card heading (default: model name)
        # tool_name="collect_sessionform",        # Tool name (default: collect_{model})
        submit_text="Submit",  # Button label (default: "Submit")
        on_submit=submit_input,  # Optional callback
    )
]

databy_file_inputs: list = [
    FileUpload(
        name="Upload File",
        description="Manually upload your dataset to clean.",
        drop_label="Drop files here. Acceptable filetype extensions: csv, xlsx, parquet, pdf, HTML, img/jpeg.",
    )
    # LocalUploadDataset(
    #     name="Upload Dataset",  # App name (used in tool routing)
    #     max_file_size=10 * 1024 * 1024,  # 10 MB default, enforced server-side
    #     title="File Upload",  # Heading shown in the UI
    #     description="Drop files to...",  # Description text below the heading
    #     drop_label="Drop files here",  # Label inside the drop zone
    # )
]
