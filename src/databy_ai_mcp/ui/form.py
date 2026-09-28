from pathlib import Path

from fastmcp.apps.file_upload import FileUpload
from fastmcp.apps.form import FormInput

from .schemas import DatabySession, DatasetFile, SessionForm
from .types import BusinessDomain, CleanState

session = DatabySession(
    metadata=SessionForm(
        business_domain=BusinessDomain.TRANSACTIONS,
        objective="Clean transaction data",
        clean_state=CleanState.MESS,
    ),
    files=[
        DatasetFile(
            filename="transactions.csv",
            content_type="text/csv",
            size_bytes=125_000,
            path=Path("data/transactions.csv"),
        )
    ],
    status="ready",
)

databy_form = FormInput(
    model=SessionForm,
    name="Session Form",
    title="Start Session",
    submit_text="Submit",
)

databy_file_upload = FileUpload(
    name="Upload Dataset",
    max_file_size=10 * 1024 * 1024,
    title="Upload Dataset",
    description=("Upload a CSV, XLSX, Parquet, HTML, or PDF dataset " "for analysis."),
    drop_label=("Drop a CSV, XLSX, Parquet, HTML, or PDF file here."),
)


def create_session(metadata: SessionForm) -> DatabySession:
    return DatabySession(
        metadata=metadata,
        status="waiting_for_file",
    )


def attach_file(
    session: DatabySession,
    *,
    filename: str,
    content_type: str | None = None,
    size_bytes: int | None = None,
    path: Path | None = None,
) -> DatabySession:
    session.files.append(
        DatasetFile(
            filename=filename,
            content_type=content_type,
            size_bytes=size_bytes,
            path=path,
        )
    )
    session.status = "ready" if session.is_ready else "waiting_for_file"
    return session
