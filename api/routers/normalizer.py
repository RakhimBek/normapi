import shutil
import json
import uuid
import requests
import subprocess

from pathlib import Path
from fastapi import APIRouter, File, UploadFile
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

        # subprocess.call(
        #    f'onmt_translate -gpu 1  -batch_size 10  -beam_size 20   -model models/gorod/model.pt  \
        #    -src {good_filepath}   -output gorod{good_filepath}.csv  -min_length  0  \
        #    -stepwise_penalty    -coverage_penalty summary  -beta 5    -length_penalty wu  -alpha 0.9  \
        #    -block_ngram_repeat 0   -ignore_when_blocking "." "<t>" "</t>"',
        #    shell=True
        # )

        subprocess.call(f'head -c 5 {good_filepath} > gorod{good_filepath}', shell=True)

        return FileResponse(f'gorod{good_filepath}')

    except Exception as e:
        print(e)
        # return {"status": "bad"}
        return FileResponse(f'gorod{good_filepath}')


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
