import os
import json
import uuid
import requests

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

        return json.loads(response.text)

    except Exception as e:
        print(e)
        return {
            "status": "FAILURE"
        }


@ya.get('/api/ya/claims/create')
def create():
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
                        "name": "Rakhim",
                        "phone": "+71234561234"
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
                        "name": "Rakhim",
                        "phone": "+71234561234"
                    },
                    "type": "destination",
                    "address": {
                        "country": "Россия",
                        "description": "",
                        "fullname": "Омская область, Оконешниковский район, д. Язово, д. 12",
                        "shortname": "Омская область, Оконешниковский район, д. Язово, д. 12",
                        "street": "Карла Маркса",
                        "building": "д. 12",
                        "coordinates": [
                            75.547103, 54.684829
                        ]
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

        return json.loads(response.text)

    except Exception as e:
        print(e)
        return {
            "status": "FAILURE"
        }
