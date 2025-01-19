from pydantic import BaseModel


class Metadata(BaseModel):
    """
    Model for information on users cloud storages to be displayed
    """
    storage_name: str
    storage_used: int
    capacity: int
    storage_available: int
    largest_file: str
    number_of_files: int
    largest_folder: str
    number_of_folders: int
    number_of_duplicates: int
    storage_used_by_duplicates: int
    oldest_file: str
    last_modified: int