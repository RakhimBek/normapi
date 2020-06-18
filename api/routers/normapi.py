"""Normalize module routings

"""
import re
import shutil
import time
from pathlib import Path

import numpy as np
import pandas as pd
from fastapi import Request, APIRouter, File, UploadFile
from pydantic import BaseModel
from starlette.responses import FileResponse
from starlette.templating import Jinja2Templates

norm_api = APIRouter()


@norm_api.get('/')
def home(request: Request):
    print('home request')
    templates = Jinja2Templates(directory='templates')
    return templates.TemplateResponse('index.html', {'request': request, 'id': 'Hi!'})


class RequestBody(BaseModel):
    """
      normalize RequestBody
    """
    string: str


@norm_api.post("/api/normalize/")
def normalize(body: RequestBody):
    """Normalizes the string set by the user.

    Args:
        body: User string.

    Returns:
        Processed user string.

    """
    bad = pd.DataFrame([['1', body.string]], columns=['id', 'address'])
    result = normalize_1(bad)['new_str'][0]
    return {
        "string": result
    }


@norm_api.post("/api/file/upload/")
async def create_upload_file(file: UploadFile = File(...)):
    """Loads the passed file and performs processing.

    Args:
        file: A csv file that has an 'address' field that contains data that needs to be preprocessed.

    Returns:
        A new file with the original strings and the result of processing.

    """
    start_time = time.time()
    print('/api/file/upload/')

    save_upload_file(file, Path(file.filename))
    res = 'result_cifrovizatori.csv'

    process(file.filename, res)
    e = int(time.time() - start_time)
    print('{:02d}:{:02d}:{:02d}'.format(e // 3600, (e % 3600 // 60), e % 60))
    print(e)
    return {'filename': res}


@norm_api.get('/api/file/result_cifrovizatori')
async def get_file():
    """Returns a new file

    Returns:
        Returns a new file

    """
    return FileResponse('result_cifrovizatori.csv')


def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    try:
        with destination.open('wb') as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()


def process(filename, result_filename) -> None:
    bad = pd.read_csv(filename, sep=';')
    normalize_1(bad).to_csv(result_filename, sep=';')


def normalize_1(df) -> pd.DataFrame:
    """Normalizes administrative units.

        Args:
            df: DataFrame.

        Returns:
            DataFrame.

        """
    df['new_str'] = df['address']
    new_col = df['address']

    # normalize column data
    new_col = new_col.str.replace('I', '1')
    new_col = new_col.str.replace('II', '2')
    new_col = new_col.str.replace('III', '3')
    new_col = new_col.str.replace('IV', '4')
    new_col = new_col.str.replace('V', '5')
    new_col = new_col.str.replace('VI', '6')
    new_col = new_col.str.replace('VII', '7')
    new_col = new_col.str.replace('VIII', '8')
    new_col = new_col.str.replace('IX', '9')
    new_col = new_col.str.replace('X', '10')
    new_col = new_col.str.replace('XI', '11')
    new_col = new_col.str.replace('XII', '12')
    new_col = new_col.str.replace('XIII', '13')

    new_col = new_col.str.lower()

    # Г
    new_col = new_col.str.replace(r'[,; /.]гор\.|г\.|[,; /]г ', ' город ')

    # Д дом, деревня
    new_col = new_col.apply(lambda s: re.sub(r'[,; .]д[. ]+([0-9/]+[а-я]?)[,. ]', r' дом \1 ', s))
    new_col = new_col.apply(lambda s: re.sub(r'[,; .]д[. ]+([а-яА-Я -]+)', r' деревня \1 ', s))
    new_col.str.replace(r'[,; /.]дер\.', ' деревня ')

    # К
    new_col = new_col.str.replace(r'[,; /.]каб\.', ' кабинет ')
    new_col = new_col.str.replace(r'[,; /.]корп\.|[,; /]корп ', ' кабинет ')
    new_col = new_col.str.replace(r'[,; /.]ком\.|[,; /]ком ', ' комната ')
    new_col = new_col.str.replace(r'[,; /.]кв\.', ' квартира ')
    new_col = new_col.str.replace(r'[,; /.]кв-л.\.', ' квартал ')

    # Н
    new_col = new_col.str.replace(r'[,; /.]наб\.', ' набережная ')

    # О
    new_col = new_col.str.replace(r'[,; /.]обл\.', ' область ')
    new_col = new_col.str.replace(r'[,; /.]обл,', ' область,')

    # П
    new_col = new_col.str.replace(r'[,; /.]пос\.|[,; /]поселок|[,; /]п\.|[,; /]п ', ' поселок ')
    new_col = new_col.str.replace(r'[,; /.]пом\.', ' помещение ')
    new_col = new_col.str.replace(r'[,; /.]пер\.', ' переулок ')
    new_col = new_col.str.replace(r'[,; /.]пр-кт\.', ' проспект ')

    # Р
    new_col = new_col.str.replace(r'[,; /.]р-н|[,; /]р-он', ' район ')

    # С село, строение
    new_col = new_col.str.replace(r'[,; /.]стр\.', ' строение ')
    new_col = new_col.str.replace(r'[,; /.]с\.|[,; /.]с ', ' село ')

    # У
    new_col = new_col.str.replace(r'[,; /.]ул\.|[,; /]ул ', ' улица ')

    # Ш
    new_col = new_col.str.replace(r'[^а-яА-Я]ш\.|[^а-яА-Я]ш ', ' шоссе ')

    # add new column
    df['new_str'] = new_col
    return df


def process_dataframe(bad) -> pd.DataFrame:
    street = r'(ул\.?\s\w+(\s\w+)?|улица\s\w+(\s\w+)?|\w+(\s\w+)?\sулица|\w+(\s\w+)?\sул\.?)'
    area = r'(обл\.?\s\w+|область\s\w+|\w+\sобласть|\w+\sобл\.?)'

    new_file = pd.DataFrame()
    new_file['id'] = bad['id']
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
    return new_file
