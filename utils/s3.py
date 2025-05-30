import boto3
import boto3.exceptions
from config import settings


class S3Client:
    def __init__(self):
        self.boto3_client = self._create_s3_client()

    @staticmethod
    def _create_s3_client():
        """
        Create an S3 client.
        """
        return boto3.client(
            service_name="s3",
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

    def upload_file(self, file_content, name, bucket_name):
        """
        Upload a file to S3.
        """
        try:
            self.boto3_client.put_object(
                Bucket=bucket_name, Key=name, Body=file_content
            )
        except boto3.exceptions.S3UploadFailedError as e:
            raise Exception(f"Failed to upload file: {e}")
        return f"https://{bucket_name}.s3.amazonaws.com/{name}"

    def get_file_content(self, name: str, bucket_name: str):
        """
        Get the content of a file from S3.
        """
        try:
            response = self.boto3_client.get_object(Bucket=bucket_name, Key=name)
            return response["Body"].read()
        except boto3.exceptions.S3DownloadFailedError as e:
            raise Exception(f"Failed to download file: {e}")
