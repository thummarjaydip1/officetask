from fastapi import FastAPI, Request
from database.database import engine,Base
from fastapi.staticfiles import StaticFiles

from routers.user_router import router as user_router
from routers.product_router import router as product_router
from routers.order_router import router as order_router
from routers.wishlist_router import router as wishlist_router
from routers.cart_router import router as cart_router
from routers.review_router import router as review_router
from routers.template_router import router as template_router

import time

app = FastAPI(
    title = "FASTAPI",
    description = "<b> FASTAPI IN JWT AUTHENTICATION AND E-COMMERCE API, <br /> <br /> Like a User, Product, Wishlist, Cart, Order Management System. </b>"
)

@app.middleware("http")
async def process(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    end_time = time.time()
    process_time = end_time - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/")
def home():
    return "FASTAPI FULL EXAMPLE..."


Base.metadata.create_all(bind = engine)

app.mount(
    "/media",
    StaticFiles(directory="media"),
    name="media"
)

app.include_router(user_router)

app.include_router(product_router)

app.include_router(order_router)

app.include_router(wishlist_router)

app.include_router(cart_router)

app.include_router(review_router)

app.include_router(template_router)