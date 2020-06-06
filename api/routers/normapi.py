"""Backup Cloud Storage module routings

"""

from fastapi import APIRouter, File, UploadFile


norm_api = APIRouter()


@norm_api.get("/")
def home():
    return {"message": "Hello, Man!"}


@norm_api.post("api/file/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}


@norm_api.post("/api/file/upload/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}
