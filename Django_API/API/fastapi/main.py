from fastapi import FastAPI
from databases.database import engine,Base
from fastapi.staticfiles import StaticFiles

from routers.router import router as student_router

app = FastAPI()

@app.get("/")
def home():
    pass

Base.metadata.create_all(bind=engine)

app.mount(
    "/media",
    StaticFiles(directory="media"),
    name="media"
)

app.include_router(student_router)