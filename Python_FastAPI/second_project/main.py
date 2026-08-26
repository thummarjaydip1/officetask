from fastapi import FastAPI
from databases.database import engine, Base
from models.model import *

from routers.category_router import router as categories_router
from routers.product_router import router as product_router
from routers.order_router import router as order_router

app = FastAPI()


Base.metadata.create_all(bind=engine)

app.include_router(categories_router)
app.include_router(product_router)
app.include_router(order_router)