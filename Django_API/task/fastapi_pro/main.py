from fastapi import FastAPI, Depends, File, UploadFile
from databases.database import engine,Base
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient
from models.model import *
from typing import Annotated
from routers.category_router import router as category_router
from routers.product_router import router as product_router


app = FastAPI()


client = TestClient(app)

@app.get("/", tags=["Default"] ,name="normal api", status_code=200)
def home():
    return {"message" : "Welcome to home page"}

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message" : "Welcome to home page"}


# @app.post("/files")
# def upload_file(file : UploadFile):
#     return file.filename

# @app.post("/fl")
# def upd_file(file : Annotated[bytes, File()]):
#     return {"file size" : len(file)}


Base.metadata.create_all(bind = engine)

app.mount(
    "/media",
    StaticFiles(directory="media"),
    name="media"
)

app.include_router(
    category_router
)

app.include_router(
    product_router
)