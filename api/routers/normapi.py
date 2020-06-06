"""Backup Cloud Storage module routings

"""
import re
import shutil
from pathlib import Path
import pandas as pd
import numpy as np

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
    save_upload_file(file, Path(file.filename))
    process()
    return {"filename": file.filename}


def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()


def process() -> None:
    street = r'(ул\.?\s\w+(\s\w+)?|улица\s\w+(\s\w+)?|\w+(\s\w+)?\sулица|\w+(\s\w+)?\sул\.?)'
    area = r'(обл\.?\s\w+|область\s\w+|\w+\sобласть|\w+\sобл\.?)'
    bad = pd.read_csv('bad.csv', sep=';')
    new_file = pd.DataFrame()
    new_file['address'] = bad['address']
    bad['address'] = bad['address'].str.replace('I', '1')
    bad['address'] = bad['address'].str.replace('II', '2')
    bad['address'] = bad['address'].str.replace('III', '3')
    bad['address'] = bad['address'].str.replace('IV', '4')
    bad['address'] = bad['address'].str.replace('V', '5')
    bad['address'] = bad['address'].str.replace('VI', '6')
    bad['address'] = bad['address'].str.replace('VII', '7')
    bad['address'] = bad['address'].str.replace('VIII', '8')
    bad['address'] = bad['address'].str.replace('IX', '9')
    bad['address'] = bad['address'].str.replace('X', '10')
    bad['address'] = bad['address'].str.replace('XI', '11')
    bad['address'] = bad['address'].str.replace('XII', '12')
    bad['address'] = bad['address'].str.replace('XIII', '13')

    bad['index'] = bad['address'].str.extract('([0-9][0-9][0-9]+)')
    bad['index'] = bad['index'].replace(np.nan, '', regex=True)
    bad['address'] = bad['address'].str.replace('([0-9][0-9][0-9]+)', '')

    bad['city'] = bad['address'].str.extract(r'(г\.?\ ?[А-Я][а-яА-Я-]+)')
    bad['city'] = bad['city'].replace(np.nan, '', regex=True)
    bad['address'] = bad['address'].str.replace(r'(г\.?\ ?[а-яА-Я-]+)', '')

    bad['hous'] = bad['address'].str.extract(r'(д\.\ ?[0-9]+[а-яА-Я]?|дом\ ?[0-9]+[а-яА-Я]?)')
    bad['hous'] = bad['hous'].replace(np.nan, '', regex=True)
    bad['address'] = bad['address'].str.replace(r'(д\.\ ?[0-9]+[а-яА-Я]?|дом\ ?[0-9]+[а-яА-Я]?)', '')

    bad['favella'] = bad['address'].str.extract(r'(д\.\ ?[а-яА-Я-]+)')
    bad['favella'] = bad['favella'].replace(np.nan, '', regex=True)
    bad['address'] = bad['address'].str.replace(r'(д\.\ ?[а-яА-Я-]+)', '')

    bad['lane'] = bad['address'].str.extract(r'(пер\.?[еулок]*\ ?[^ ,]+)')
    bad['lane'] = bad['lane'].replace(np.nan, '', regex=True)
    bad['address'] = bad['address'].str.replace(r'(пер\.?[еулок]*\ ?[^ ,]+)', '')

    k = list()
    for i in bad['address']:
        match = re.search(street, i)
        if match:
            k.append(match[0])
            i.replace(street, '')
        else:
            k.append('')

    bad['street'] = k

    bad['area'] = bad['address'].str.extract(area)
    bad['area'] = bad['area'].replace(np.nan, '', regex=True)
    bad['address'] = bad['address'].str.replace(area, '')

    new_file['new_str'] = bad['index'].astype(str) + ", " + bad['area'] + ", " + bad['city'] + ", " + bad['street'] + \
                          ", " + bad['hous'] + ", " + bad['favella']
    new_file.to_csv('result_cifrovizatori.csv')
