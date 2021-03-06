import json
import os
import shutil
import subprocess
import time
import uuid
from pathlib import Path

import requests
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel

normalizer = APIRouter()


def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
	try:
		with destination.open('wb') as buffer:
			shutil.copyfileobj(upload_file.file, buffer)
	finally:
		upload_file.file.close()


def call(model_name, name):
	subprocess.run(
		f'onmt_translate -batch_size 10 -beam_size 20 -model ../models/{model_name}/model.pt \
           -src {name} -output {model_name}{name} -min_length 0 \
           -stepwise_penalty -coverage_penalty summary -beta 5 -length_penalty wu -alpha 0.9  \
           -block_ngram_repeat 0 -ignore_when_blocking "." "<t>" "</t>"',
		shell=True
	)
	print(f'call {model_name}')


def wait_for_files(good_filepath):
	while not os.path.exists(f'gorod{good_filepath}'):
		time.sleep(1)

	while not os.path.exists(f'rayon{good_filepath}'):
		time.sleep(1)

	while not os.path.exists(f'street{good_filepath}'):
		time.sleep(1)
	print('wait_for_files')


class RequestBody(BaseModel):
	"""
	  normalize RequestBody
	"""
	string: str


@normalizer.post("/api/normalizer/single")
def normalize(body: RequestBody):
	"""
	Normalizes the string set by the user.

	Args:
		body: User string.

	Returns:
		Processed user string.

	"""
	return body


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

		call('gorod', good_filepath)
		call('rayon', good_filepath)
		call('street', good_filepath)

		wait_for_files(good_filepath)

		subprocess.run(
			f'paste gorod{good_filepath} rayon{good_filepath} street{good_filepath} \
             | sed "s/[a-z<>/]//g" > res{good_filepath}',
			shell=True
		)

		# data = pd.read_csv(good_filepath, delimiter=';', header=None)
		# values = list(map(lambda x: search_in_fias(x[0]), data.loc[:, [0]].values))
		# pd.DataFrame(data=values).to_csv('res' + suffix + '.csv', sep=';', index=False, header=False)

		return FileResponse('res' + good_filepath)
	# return FileResponse(f'gorod{good_filepath}')

	except Exception as e:
		print(e)
		# return {"status": "bad"}
		return None


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
