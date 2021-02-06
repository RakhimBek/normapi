import os
import shutil
import json
import uuid
import requests
import pandas as pd

from pathlib import Path
from pydantic import BaseModel
from fastapi import Request, APIRouter, File, UploadFile
from starlette.responses import FileResponse

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

        data = pd.read_csv(good_filepath, delimiter=';', header=None)

        values = list(map(lambda x: search_in_fias(x[0]), data.loc[:, [0]].values))
        pd.DataFrame(data=values).to_csv('res' + suffix + '.csv', sep=';', index=False, header=False)

        return FileResponse('res' + suffix + '.csv')

    except Exception as e:
        print(e)
        # return {"status": "bad"}
        return FileResponse('res' + suffix + '.csv')


def search_in_fias(text):
    url = 'https://fias.nalog.ru/Search/Searching?text=' + text

    payload = {}
    headers = {
        'mode': 'cors'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    try:
        return json.loads(response.text)[0]['PresentRow']
    except Exception as e:
        return 'No data found.'
