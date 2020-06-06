import uvicorn
from fastapi import FastAPI, File, UploadFile
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from api.api import router as api_router

from settings import HOST, PORT, PROJECT_NAME, DEBUG, API_VERSION, API_PREFIX, OAS_FILENAME
from pathlib import Path

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
    uvicorn.run(app, host=HOST, port=PORT)
