from fastapi import APIRouter, Depends, Body, UploadFile
from utils.s3 import S3Client
from src.files.services import FileService
from src.files.schemas.files_schemas import FileSchema


router = APIRouter(prefix="/files", tags=["files"])


@router.post("/upload/contet")
async def upload_file(payload: FileSchema = Body(...)):
    """
    Upload a file to the server.
    """
    service = FileService(S3Client(), None)
    private_file_url = await service.upload_file(
        payload.content,
        payload.file_type,
    )
    return {
        "file_url": private_file_url
    }
    
@router.post("/upload/file")
async def upload_file_object(file: UploadFile):
    """
    Upload a file to the server.
    """
    service = FileService(S3Client(), None)
    _, file_type = file.filename.split(".")
    private_file_url = await service.upload_file(file.file, file_type)
    return {
        "file_url": private_file_url
    }


@router.get("/download")
async def get_filfe_content():
    """
    Get the content of a file.
    """
    pass
