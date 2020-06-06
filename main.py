from fastapi import FastAPI, File, UploadFile

app = FastAPI()

#domain where this api is hosted for example : localhost:5000/docs to see swagger documentation automagically generated.


@app.get("/")
def home():
    return {"message":"Hello, Man!"}

@app.post("api/file/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}
