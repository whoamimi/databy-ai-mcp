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
