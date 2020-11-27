import os
import json
import uuid
import requests

from pydantic import BaseModel
from fastapi import Request, APIRouter, File, UploadFile

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

        claims = json.loads(response.text)['claims'];
        print(list(map(lambda claim: {'id': claim['id'], 'version': claim['revision']}, claims)))

        return {
            'url': url,
            'response': json.loads(response.text)
        }

    except Exception as e:
        print(e)
        return {
            "status": "FAILURE"
        }


class CreateRq(BaseModel):
    point: list
    text: str


@ya.post('/api/ya/claims/create')
def create(body: CreateRq):
    auth_key = os.getenv('YA_AUTH_KEY', 'NOT_A_KEY')

    try:
        url = 'https://b2b.taxi.yandex.net/b2b/cargo/integration/v2/claims/create'

        payload = {
            "client_requirements": {
                "cargo_loaders": 0,
                "taxi_class": "courier"
            },
            "items": [
                {
                    "cost_currency": "RUR",
                    "cost_value": "100",
                    "pickup_point": 1,
                    "droppof_point": 2,
                    "quantity": 1,
                    "size": {
                        "height": 0.4,
                        "length": 0.4,
                        "width": 0.2
                    },
                    "title": "Еда.",
                    "weight": 1
                }
            ],
            "optional_return": False,
            "route_points": [
                {
                    "point_id": 1,
                    "visit_order": 1,
                    "contact": {
                        "name": "Иван",
                        "phone": "+79138886060"
                    },
                    "type": "source",
                    "address": {
                        "city": "Томск",
                        "coordinates": [
                            84.94564528465693,
                            56.493949481830924
                        ],
                        "country": "Россия",
                        "description": "",
                        "comment": "ЮЖАНЕ, ресторан, Карла Маркса, 23а",
                        "fullname": "ЮЖАНЕ, ресторан, Карла Маркса, 23а",
                        "shortname": "ЮЖАНЕ, ресторан, Карла Маркса, 23а",
                        "street": "Карла Маркса",
                        "building": "23а"
                    }
                },
                {
                    "point_id": 2,
                    "visit_order": 2,
                    "contact": {
                        "name": "Иван",
                        "phone": "+79138886060"
                    },
                    "type": "destination",
                    "address": {
                        "country": "Россия",
                        "description": "",
                        "fullname": body.text,
                        "shortname": body.text,
                        "street": body.text,
                        "building": body.text,
                        "coordinates": body.point
                    }
                }
            ]
        }

        headers = {
            'Authorization': f'Bearer {auth_key}',
            'Accept-Language': 'ru'
        }

        response = requests.request(
            "POST",
            url,
            headers=headers,
            data=json.dumps(payload),
            params={
                "request_id": str(uuid.uuid4())
            }
        )

        return {
            'url': url,
            'request': json.loads(response.text),
            'response': payload
        }

    except Exception as e:
        print(e)
        return {
            "status": "FAILURE"
        }


def cancel_request(cid, version):
    auth_key = os.getenv('YA_AUTH_KEY', 'NOT_A_KEY')
    url = 'https://b2b.taxi.yandex.net/b2b/cargo/integration/v1/claims/cancel'

    payload = {
        "cancel_state": "free",
        "version": version
    }

    headers = {
        'Authorization': f'Bearer {auth_key}',
        'Accept-Language': 'ru'
    }

    params = {
        'claim_id': cid
    }

    return {
        'request': payload,
        'response': json.loads(
            requests.request("POST", url, headers=headers, data=json.dumps(payload), params=params).text),
    }


@ya.get('/api/ya/claims/cancel')
def cancel_all():
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

        claims = json.loads(response.text)['claims']

        responses = list(map(lambda claim: cancel_request(claim['id'], claim['revision']), claims))

        return {
            'responses': responses
        }

    except Exception as e:
        print(e)
        return {
            "status": "FAILURE"
        }


def accept_request(cid):
    auth_key = os.getenv('YA_AUTH_KEY', 'NOT_A_KEY')
    url = 'b2b.taxi.yandex.net/b2b/cargo/integration/v1/claims/accept'
    payload = {
        "version": 1
    }

    headers = {
        'Authorization': f'Bearer {auth_key}',
        'Accept-Language': 'ru'
    }

    params = {
        'claim_id': cid
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload), params=params)

    return {
        'request': payload,
        'response': json.loads(response.text)
    }


@ya.get('/api/ya/claims/accept/')
def accept_all():
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

        claims = json.loads(response.text)['claims']

        responses = list(map(lambda claim: accept_request(claim['id']), claims))

        return {
            'responses': responses
        }

    except Exception as e:
        print(e)
        return {
            "status": "FAILURE"
        }
