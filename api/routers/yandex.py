import os
import json

from fastapi import Request, APIRouter, File, UploadFile
import requests

ya = APIRouter()


@ya.get('/api/ya/claims/search/active/')
def search():
    auth_key = os.getenv('YA_AUTH_KEY', 'NOT_A_KEY')

    try:
        url = 'https://b2b.taxi.yandex.net/b2b/cargo/integration/v2/claims/search/active'

        payload = {
            "limit": 10,
            "offset": 0
        }

        headers = {
            'Authorization': f'Bearer {auth_key}',
            'Accept-Language': 'ru'
        }

        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

        return json.loads(response.text)

    except Exception as e:
        print(e)
        return {
            "status": "FAILURE"
        }
