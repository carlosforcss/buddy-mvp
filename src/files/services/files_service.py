from uuid import uuid4
from config import settings
from utils.s3 import S3Client


class FileService:
    """
    Upload a service to S3 and create a presigned URL for it.
    """
    
    def __init__(self, s3_client: S3Client, db_client):
        self.s3_client = s3_client
        self.db_client = db_client 
         
    async def upload_file(self, file_content, file_type, file_name=None, bucket_name=None):
        """
        Upload a file to S3 and create a presigned URL for it.
        """
        if not bucket_name:
            bucket_name = settings.DEFAULT_BUCKET_NAME
        if not file_name:
            file_name = f"{uuid4()}.{file_type}"
        
        # Upload the file to S3
        private_url = self.s3_client.upload_file(file_content, file_name, bucket_name)
        return private_url

    async def get_content(self, file_name, bucket_name=None):
        """
        Get the content of a file from S3.
        """
        if not bucket_name:
            bucket_name = settings.S3_BUCKET_NAME
        return self.s3_client.get_file_content(file_name, bucket_name)
