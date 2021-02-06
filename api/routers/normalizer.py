import os
import shutil
import json
import uuid
import requests

from pathlib import Path
from pydantic import BaseModel
from fastapi import Request, APIRouter, File, UploadFile

normalizer = APIRouter()


def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    try:
        with destination.open('wb') as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()


@normalizer.post("/api/normalizer/file/")
async def create_upload_file(file: UploadFile = File(...)):
    """Loads the passed file and performs processing.

    Args:
        file: A csv file that has an 'address' field that contains data that needs to be preprocessed.

    Returns:
        A new file with the original strings and the result of processing.

    """
    print('/api/file/upload/')

    try:
        suffix = str(uuid.uuid4()).replace('-', '').upper()
        good_filepath = suffix + '.csv'
        save_upload_file(file, Path(good_filepath))

        return {'filename': suffix}

    except Exception as e:
        print(e)
        return {"status": "bad"}
