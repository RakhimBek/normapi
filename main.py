from fastapi import FastAPI, File, UploadFile
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

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

@app.get("/")
def home():
    return {"message":"Hello, Man!"}

@app.post("api/file/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}

@app.post("/api/file/upload/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}
