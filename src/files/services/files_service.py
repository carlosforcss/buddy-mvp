from uuid import uuid4
from config import settings
from src.files.repositories import FilesRepository
from utils.s3 import S3Client


class FileService:
    """
    Upload a service to S3 and create a presigned URL for it.
    """

    def __init__(
        self,
        s3_client: S3Client,
        files_repository: FilesRepository,
        logger: "utils.logger.Logger",
    ):
        self.s3_client = s3_client
        self.files_repository = files_repository
        self.logger = logger

    async def upload_file(
        self, file_content, file_type, file_name=None, bucket_name=None
    ):
        """
        Upload a file to S3 and create a presigned URL for it.
        """
        self.logger.info(f"Uploading file to S3: {file_name} of type {file_type}")
        if not bucket_name:
            bucket_name = settings.DEFAULT_BUCKET_NAME
        if not file_name:
            file_name = f"{uuid4()}.{file_type}"

        # Upload the file to S3
        self.s3_client.upload_file(file_content, file_name, bucket_name)
        new_file = await self.files_repository.create(
            file_name=file_name,
            bucket_name=bucket_name,
        )

        return new_file

    async def get_file_content(self, file_id: int):
        """
        Get the content of a file from S3.
        """
        self.logger.info(f"Getting file content from S3: {file_id}")
        file = await self.files_repository.get_by_id(file_id)
        return self.s3_client.get_file_content(file.name, file.bucket), file.name
