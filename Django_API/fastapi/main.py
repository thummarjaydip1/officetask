from fastapi import FastAPI, Request, Depends
from database.database import engine,Base
from fastapi.staticfiles import StaticFiles

from models.model import *
from database.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
import time

from routers.user_router import router as user_router
from routers.product_router import router as product_router
from routers.order_router import router as order_router
from routers.order_return_router import router as order_return_router
from routers.wishlist_router import router as wishlist_router
from routers.cart_router import router as cart_router
from routers.review_router import router as review_router
from routers.template_router import router as template_router


app = FastAPI(
    title = "FASTAPI",
    description = ""
    "<b> FASTAPI IN JWT AUTHENTICATION AND E-COMMERCE API, "
    "<br /> <br /> " \
    "Like a User, Product, Review, Wishlist, Cart, Order, Payment Management System. </b>" ""
)

@app.middleware("http")
async def process(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    end_time = time.time()
    process_time = end_time - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# http://127.0.0.1:8000/dashboard
@app.get("/dashboard", tags = ["Dashboard"])
def dashboard_api(
    db : Session = Depends(get_db)
):    
    total_users = db.query(User).count()

    total_products = db.query(Product).count()

    total_orders = db.query(Order).count()
    
    total_wishlists = db.query(Wishlist).count()

    total_carts = db.query(Cart).count()

    total_reviews = db.query(Review).count()

    total_return_orders = db.query(ReturnOrder).count()

    total_payments = db.query(
        func.sum(Payment.amount)
    ).scalar() or 0

    return {
        "total_users" : total_users,
        "total_products" : total_products,
        "total_orders" : total_orders,
        "total_wishlists" : total_wishlists,
        "total_carts" : total_carts,
        "total_reviews" : total_reviews,
        "total_return_order" : total_return_orders,
        "total_payments" : total_payments,
    }

Base.metadata.create_all(bind = engine)

app.mount(
    "/media",
    StaticFiles(directory="media"),
    name="media"
)

app.include_router(user_router)

app.include_router(product_router)

app.include_router(order_router)

app.include_router(order_return_router)

app.include_router(wishlist_router)

app.include_router(cart_router)

app.include_router(review_router)

app.include_router(template_router)