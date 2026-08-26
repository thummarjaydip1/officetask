from models.model import *
from databases.database import Base, engine
from routers.router import router
from fastapi import FastAPI

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/app")