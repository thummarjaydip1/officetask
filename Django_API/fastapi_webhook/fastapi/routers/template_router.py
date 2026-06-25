from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from database.database import get_db
from models.model import User, Product, Order
import requests

router = APIRouter(
    prefix = "/templates",
    tags = ["Template"]
)

template = Jinja2Templates(directory="templates")

# http://127.0.0.1:8000/templates/display
@router.get("/display")
def display(
    request: Request,
    db: Session = Depends(get_db)
):
    
    # user display
    users = db.query(User).all()

    # product display
    products = db.query(Product).all()
    
    pro_data = {}

    for product in products:
        user = db.query(User).filter( 
            User.id == product.user_id
        ).first()

        pro_data[product.id] = user.username
        

    # order display
    orders = db.query(Order).all()
    
    order_details = {}
    for order in orders:

        user_data = db.query(User).filter(
            User.id == order.user_id
        ).first()

        product_data = db.query(Product).filter(
            Product.id == order.product_id
        ).first()

        order_details[order.id] = {
            "username" : user_data.username,
            "address" : user_data.address,
            "product_name" : product_data.name,
            "image" : product_data.image,
            "price" : product_data.price
        }
    
    return template.TemplateResponse(
        request = request,
        name = "index.html",
        context = {
            "users" : users,
            "products" : products,
            "pro_data" : pro_data,
            "orders": orders,
            "order_details" : order_details
        }
    )


# http://127.0.0.1:8000/templates/pagination 
@router.get("/pagination")
def pagination_order(
    request: Request,
    page : int = 1
):
    res = requests.get(
        f"http://127.0.0.1:8000/orders/pagination/display?page={page}&size=3"
    )
    data = res.json()
    
    return template.TemplateResponse(
    request=request,
    name="pagination.html",
    context={
        "orders": data["orders"],
        "page": data["page"],
        "total": data["total"]
    }
)