from fastapi import APIRouter, HTTPException, Depends, Form, Request
from sqlalchemy.orm import Session
from email_service import order_send_email

from database.database import get_db
from models.model import Order, Product, User, Payment
from auth import get_current_user

import random
from datetime import datetime

router = APIRouter(
    prefix = "/orders",
    tags = ["Order"]
)


# http://127.0.0.1:8000/orders/add
@router.post("/add")
async def add_order(
    product_id: int = Form(...),
    quantity : int = Form(...),
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product Not Found Plaese Enter Correct Product Name")
    
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Enter more than 0(zero) qunatity")
    
    total_price = quantity * int(product.price)

    new_order = Order(
        user_id = user_id,
        product_id = product.id,
        quantity = quantity,
        total = total_price
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    await order_send_email(
        username = user.username,
        email = user.email,
        product_name = product.name,
        price = product.price,
        quantity = new_order.quantity,
        total_price = new_order.total,
        delivery_address = user.address
    )

    return {
        "message" : "Place Order Successfully",
        "order_id": new_order.id
    }


# http://127.0.0.1:8000/orders/display
@router.get("/display")
def display_order(
    request: Request,
    db: Session = Depends(get_db)
):
    orders = db.query(Order).order_by(
        Order.id.desc()
    ).all()
    data = []

    for order in orders: 

        user = db.query(User).filter(User.id == order.user_id).first()
        
        product = db.query(Product).filter(Product.id == order.product_id).first()

        data.append({
            "order_id" : order.id,
            "username" : user.username,
            "product_name" : product.name,
            "price": product.price,
            "image": str(request.base_url) + f"media/product/{product.image}",
            "quantity" : order.quantity,
            "total_price" : order.total,
            "address" : user.address
        })

    return data


# http://127.0.0.1:8000/orders/pagination/display
@router.get("/pagination/display")
def pagination_display_order(
    request : Request,
    page : int = 1,
    size : int = 3,
    db : Session = Depends(get_db)
):
    if page < 1:
        raise HTTPException(status_code=400, detail="Page must be greater than 0(zero)")
    
    if size < 1:
        raise HTTPException(status_code=400, detail="size must be greater than 0(zero)")

    total = db.query(Order).count()

    orders = db.query(Order).offset((page - 1) * size).limit(size).all()
    
    data = []

    for order in orders:
        
        user = db.query(User).filter(User.id == order.user_id).first()
        product = db.query(Product).filter(Product.id == order.product_id).first()

        data.append({
            "order_id" : order.id,
            "product_image" : str(request.base_url) + f"media/product/{product.image}",
            "product_name" : product.name,
            "product_price" : product.price,
            "username" : user.username,
            "address" : user.address
        })
    return {
        "page" : page,
        "size" : size,
        "total" : total,
        "orders" : data
    }


# http://127.0.0.1:8000/orders/my-orders
@router.get("/my-orders")
def display_my_order(
    request: Request,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    orders = db.query(Order).filter(Order.user_id == user_id).all()
        
    data = []

    for order in orders:

        user = db.query(User).filter(User.id == order.user_id).first()
        product = db.query(Product).filter(Product.id == order.product_id).first()

        data.append({
            "id" : order.id,
            "username" : user.username,
            "product_name" : product.name,
            "product_price" : product.price,
            "product.image" : str(request.base_url) + f"media/product/{product.image}",
            "address" : user.address
        })
    return data


# http://127.0.0.1:8000/orders/update/{id}
@router.put("/update/{id}")
def update_order(
    id: int,
    quantity : int = Form(...),
    user_id : str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = db.query(Order).get(id)

    if not order:
        raise HTTPException(status_code=404, detail="Order Not Found")
    
    if order.user_id != user_id:
        raise HTTPException(status_code=400, detail="you can update own order please check your order")
    
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Enter more than 0(zero) quantity") 
    
    product = db.query(Product).filter(Product.id == order.product_id).first()

    total_price = quantity * int(product.price)
    
    order.quantity = quantity
    order.total = total_price
        
    db.commit()
    db.refresh(order)

    return {
        "message" : "Order Update Successfully",
        "order_id" : order.id
    }


# http://127.0.0.1:8000/orders/delete/{id}
@router.delete("/delete/{id}")
def delete_order(
    id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)    
):
    data = db.query(Order).get(id)

    if not data: 
        raise HTTPException(status_code=404, detail='Order not found')
    
    if data.user_id != user_id:
        raise HTTPException(status_code=404, detail="you can delete own order please check your order id")
 
    db.delete(data)
    db.commit()

    return {"message" : "Order Deleted Successfully"}


# http://127.0.0.1:8000/orders/bill/{id}
@router.get("/bill/{id}")
def bill_system(
    request : Request,
    id : int,
    user_id : int = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    order = db.query(Order).get(id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.user_id != user_id:
        raise HTTPException(status_code=404, detail="you can check only own order bill")
    
    data = []

    if order:

        product = db.query(Product).filter(Product.id == order.product_id).first()
        user = db.query(User).filter(User.id == order.user_id).first()

        data.append({
            "order_id" : order.id,
            "product_name" : product.name,
            "product_price" : product.price,
            "product_image" : str(request.base_url) + f"media/product/{product.image}",
            "quantity" : order.quantity,
            "total_price" : order.total,
            "username" : user.username,
            "email" : user.email,
            "address" : user.address
        })

    return data


# http://127.0.0.1:8000/orders/search
@router.get("/search")
def search_order(
    request : Request,
    product_name : str = None,
    user_id : int = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.name.contains(product_name)
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    orders = db.query(Order).filter(
        Order.product_id == product.id,
        Order.user_id == user_id
    ).all()

    if not orders:
        raise HTTPException(status_code=404, detail="Order not found")

    data = []

    for order in orders:

        product = db.query(Product).get(order.product_id)
        user = db.query(User).get(order.user_id)

        # product = db.query(Product).filter(Product.id == order.product_id).first()
        # user = db.query(User).filter(User.id == order.user_id).first()

        data.append({
            "order_id" : order.id,
            "username" : user.username,
            "product_name" : product.name,
            "product_price" : product.price,
            "image" : str(request.base_url) + f"media/product/{product.image}",
            "delivary_address" : user.address
        })
    
    return data


# ************Function************
# Transaction Id Generate Function
def generate_transaction_id():
    random_number = random.randint(1000,9999)
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    transaction_id = f"TXN{current_time}{random_number}"
    return transaction_id


# http://127.0.0.1:8000/orders/payment/create
@router.post("/payment/create")
def order_payment_create(
    order_id : int = Form(...),
    payment_method : str = Form(...),
    user_id : int = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="order not found")
    
    if order.user_id != user_id:
        raise HTTPException(status_code=403, detail="you can pay only own order")
    
    payment = db.query(Payment).filter(Payment.order_id == order.id).first()

    if payment:
        raise HTTPException(status_code=400, detail="Payment is already exists")
    
    allowed_method = [
        "Cash", "Card", "UPI", "Wallet", "Net Banking"
    ]

    if payment_method not in allowed_method:
        raise HTTPException(status_code=400, detail="Invalid Method")
    
    new_payment = Payment(
        order_id = order.id,
        user_id = user_id,
        amount = order.total,
        payment_method = payment_method,
        payment_status = "success",
        transaction_id = generate_transaction_id()
    )

    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    return {
        "message" : "Payment Successfully",
        "payment_id" : new_payment.id,
        "amount" : new_payment.amount,
        "payment_method" : new_payment.payment_method,
        "payment_status" : new_payment.payment_status
    }


# http://127.0.0.1:8000/orders/payment/show/{id}
@router.get("/payment/show/{id}")
def payment_show(
    request : Request,
    id : int,
    user_id : int = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    payment = db.query(Payment).filter(Payment.id == id).first()

    if not payment:
        raise HTTPException(status_code=404, detail="payment id not found")
    
    if payment.user_id != user_id:
        raise HTTPException(status_code=403, detail="you can show only your payment details")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not Found")

    order = db.query(Order).filter(Order.id == payment.order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="order not found")

    product = db.query(Product).filter(Product.id == order.product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="product not found")

    return {
        "payment_id" : payment.id,
        "order_id" : payment.order_id,
        "username" : user.username,
        "product_name" : product.name,
        "product_price" : product.price,
        "product_image" : str(request.base_url) + f"media/product/{product.image}",
        "pay_amount" : payment.amount,
        "payment_method" : payment.payment_method,
        "payment_status" : payment.payment_status,
        "transaction_id" : payment.transaction_id
    }
