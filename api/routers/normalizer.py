import json
import logging
import os
import re
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
logging.basicConfig(filename='normalizer.log', level=logging.INFO)


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

	suffix = str(uuid.uuid4()).replace('-', '').upper()
	with open(suffix, 'w') as f:
		f.write(body.string)

	call('gorod', suffix)
	call('rayon', suffix)
	call('street', suffix)

	wait_for_files(suffix)

	with open(f'gorod{suffix}', 'r') as gf:
		with open(f'rayon{suffix}', 'r') as rf:
			with open(f'street{suffix}', 'r') as sf:
				while True:
					city = gf.readline()
					area = rf.readline()
					street = sf.readline()
					if city == '' and area == '' and street == '':
						break

					city = re.sub(r'[t<>\n/]', '', city)
					city = re.sub(r'[\t ]+', ' ', city).strip().upper()

					area = re.sub(r'[t<>\n/]', '', area)
					area = re.sub(r'[\t ]+', ' ', area).strip().upper()

					street = re.sub(r'[t<>\n/]', '', street)
					street = re.sub(r'[\t ]+', ' ', street).strip().upper()

					string = ("г. " + city + ", " if city else "") \
							 + ((area + ' район, ') if area else "") \
							 + ("ул." + street if street else "")

					fias_result = search_in_fias(string)
					result = {
						'fias': fias_result,
						'city': city,
						'area': area,
						'street': street
					}

					logging.info(f'S:{body.string};{city};{area};{street};{string};{fias_result}')

	return result


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
		save_upload_file(file, Path(suffix))

		call('gorod', suffix)
		call('rayon', suffix)
		call('street', suffix)

		wait_for_files(suffix)

		with open(f'res{suffix}', 'w') as res:
			with open(f'gorod{suffix}', 'r') as gf:
				with open(f'rayon{suffix}', 'r') as rf:
					with open(f'street{suffix}', 'r') as sf:
						while True:
							city = gf.readline()
							area = rf.readline()
							street = sf.readline()
							if city == '' and area == '' and street == '':
								break

							city = re.sub(r'[t<>\n/]', '', city)
							city = re.sub(r'[\t ]+', ' ', city).strip().upper()

							area = re.sub(r'[t<>\n/]', '', area)
							area = re.sub(r'[\t ]+', ' ', area).strip().upper()

							street = re.sub(r'[t<>\n/]', '', street)
							street = re.sub(r'[\t ]+', ' ', street).strip().upper()
							string = ("г. " + city + ", " if city else "") \
									 + (area + " район, " if area else "") \
									 + ("ул." + street if street else "")

							fias_result = search_in_fias(string)
							res.write(fias_result + '\n')

							logging.info(f'M:{suffix};{city};{area};{street};{string};{fias_result}')

		return FileResponse('res' + suffix)

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
