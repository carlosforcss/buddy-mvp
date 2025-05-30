from fastapi import APIRouter, Depends, Body, UploadFile
from utils.s3 import S3Client
from utils.logger import Logger
from src.files.services import FileService
from src.files.schemas.files_schemas import FileSchema
from src.files.repositories import FilesRepository
from fastapi.responses import StreamingResponse
from io import BytesIO


router = APIRouter(prefix="/files", tags=["files"])
logger = Logger(__name__)


@router.post("/upload")
async def upload_file_object(file: UploadFile):
    """
    Upload a file to the server.
    """
    service = FileService(S3Client(), FilesRepository(logger), logger)
    _, file_type = file.filename.split(".")
    new_file = await service.upload_file(file.file, file_type)
    return FileSchema(id=new_file.id, name=new_file.name)


@router.get("/download/")
async def download_file(file_id: int):
    service = FileService(S3Client(), FilesRepository(logger), logger)
    file_content, file_name = await service.get_file_content(file_id)
    buffer = BytesIO(file_content)
    return StreamingResponse(
        buffer,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={file_name}"},
    )
