from fastapi import FastAPI
from databases.database import engine,Base
from fastapi.staticfiles import StaticFiles
from models.model import *
from routers.category_router import router as category_router
from routers.product_router import router as product_router

app = FastAPI()


Base.metadata.create_all(bind = engine)

app.mount(
    "/media",
    StaticFiles(directory="media"),
    name="media"
)

app.include_router(category_router)
app.include_router(product_router)