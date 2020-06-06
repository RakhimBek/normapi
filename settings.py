"""Settings for Backup Cloud Storage

"""
from starlette.config import Config

config = Config('.env')

# FastAPI settings
PROJECT_NAME = 'normapi'
API_VERSION = '1.0'
API_PREFIX = '/api'
OAS_FILENAME = 'openapi.json'
DEBUG = config('DEBUG', cast=bool, default=True)

HOST = config('HOST', cast=str, default='0.0.0.0')
PORT = config('PORT', cast=int, default=8888)

RESULT_FILE_NAME = 'result_cifrovizatori.csv'
