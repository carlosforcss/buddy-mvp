from src.files.models import File


class FilesRepository:
    def __init__(self, logger: "utils.logger.Logger"):
        self.logger = logger

    async def create(self, file_name: str, bucket_name: str = None):
        """
        Create a new file record in the database.
        """
        self.logger.info(
            f"Creating file record in the database: {file_name} in bucket {bucket_name}"
        )
        new_file = await File.create(name=file_name, bucket=bucket_name)
        return new_file

    async def get_by_id(self, file_id: int):
        """
        Get a file record by its ID.
        """
        self.logger.info(f"Getting file record by ID: {file_id}")
        file = await File.get(id=file_id)
        return file
