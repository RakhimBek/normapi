from pathlib import Path

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from api.api import router as api_router
from settings import API_PREFIX, API_VERSION, DEBUG, HOST, OAS_FILENAME, PORT, PROJECT_NAME

app = FastAPI(
    title=PROJECT_NAME,
    debug=DEBUG,
    version=API_VERSION,
    redoc_url=None,
    openapi_url=Path(API_PREFIX, OAS_FILENAME).as_posix(),
)

app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

if __name__ == '__main__':

    with open('environment.properties', 'w+') as f:
        f.write('HOST=213.159.209.30')
        f.write('PORT=5432')
        f.write('DATABASE=addresses')
        f.write('USER=normalizer')
        f.write('PASSWORD=1q3w2e4r5t')

    uvicorn.run(app, host=HOST, port=PORT)
