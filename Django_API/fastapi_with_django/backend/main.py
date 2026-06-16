import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from fastapi import FastAPI
from routers.product_router import router as product_router
from routers.user_router import router as user_router

app = FastAPI()

@app.get("/")
def home():
    return "Product API with Image store and User Authentication"

app.include_router(product_router)
app.include_router(user_router)