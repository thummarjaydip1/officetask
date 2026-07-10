from django import db
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session

from database.database import get_db
from models.model import *
from auth import get_current_user


router = APIRouter(
    prefix = "/return-orders",
    tags = ["Return Orders"]
)


# http://127.0.0.1:8000/return-orders/create
@router.post("/create")
def create_return_order(
    order_id : int = Form(...),
    reason : str = Form(...),
    user_id : int = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="order not found")
    
    if order.user_id != user_id:
        raise HTTPException(status_code=403, detail="you can return only your own order")
    
    exist_return_order = db.query(ReturnOrder).filter(ReturnOrder.order_id == order_id).first()

    if exist_return_order:
        raise HTTPException(status_code=400, detail="return order already exists")
    
    new_return_order = ReturnOrder(
        order_id = order_id,
        user_id = user_id,
        reason = reason
    )

    db.add(new_return_order)
    db.commit()
    db.refresh(new_return_order)
    
    return {
        "message" : "return order created successfully",
        "id" : new_return_order.id,
        "reason" : new_return_order.reason
    }


# http://127.0.0.1:8000/return-orders/display/{id}
@router.get("/display/{id}")
def display_return_order_by_id(
    request : Request,
    id : int,
    user_id : int = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    return_order = db.query(ReturnOrder).filter(ReturnOrder.id == id).first()

    if not return_order:
        raise HTTPException(status_code=404, detail="return order not found")
    
    if return_order.user_id != user_id:
        raise HTTPException(status_code=403, detail="you can view only your own return order")
    
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    order = db.query(Order).filter(Order.id == return_order.order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="order not found")

    product = db.query(Product).filter(Product.id == order.product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="product not found")

    return {
        "id" : return_order.id,
        "order_id" : return_order.order_id,
        "product_image" : str(request.base_url) + f"media/product/{product.image}",
        "product_name" : product.name,
        "product_price" : product.price,
        "quantity" : order.quantity,
        "total_amount" : order.total,
        "reason" : return_order.reason,
        "status" : return_order.status,
        "username" : user.username
    }


# http://127.0.0.1:8000/return-orders/display
@router.get("/display")
def display_return_order_by_user(
    request : Request,
    user_id : int = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    return_orders = db.query(ReturnOrder).filter(ReturnOrder.user_id == user_id).all()

    if not return_orders:
        raise HTTPException(status_code=404, detail="return order not found")

    data = []

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    for return_order in return_orders:

        order = db.query(Order).filter(Order.id == return_order.order_id).first()

        product = db.query(Product).filter(Product.id == order.product_id).first()

        data.append({
            "id" : return_order.id,
            "order_id" : return_order.order_id,
            "product_image" : str(request.base_url) + f"media/product/{product.image}",
            "product_name" : product.name,
            "product_price" : product.price,
            "quantity" : order.quantity,
            "total_amount" : order.total,
            "reason" : return_order.reason,
            "status" : return_order.status,
            "username" : user.username
        })
    
    return data


# http://127.0.0.1:8000/return-orders/update/{id}
@router.put("/update/{id}")
def update_return_order(
    id : int,
    status : str = Form(...),
    user_id : int = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    return_order = db.query(ReturnOrder).filter(ReturnOrder.id == id).first()

    if not return_order:
        raise HTTPException(status_code=404, detail="return order not found")
    
    user = db.query(User).filter(User.id == user_id).first()

    # if user.role != "admin":
        # raise HTTPException(status_code=403, detail="only admin can update return order status")

    if user.username != "jaydip":
        raise HTTPException(status_code=403, detail="only jaydip can update return order status")
    
    status_list = ["approved", "rejected", "completed"]

    if status not in status_list:
        raise HTTPException(status_code=400, detail=f"invalid status, please choose from {status_list}")

    return_order.status = status
    db.commit()

    return {
        "message" : "return order status updated successfully",
        "id" : return_order.id,
        "status" : return_order.status
    }


# http://127.0.0.1:8000/return-orders/cancel/{id}
@router.delete("/cancel/{id}")
def cancel_return_order(
    id : int,
    user_id : int = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    return_order = db.query(ReturnOrder).filter(ReturnOrder.id == id).first()

    if not return_order:
        raise HTTPException(status_code=404, detail="return order not found")

    if return_order.user_id != user_id:
        raise HTTPException(status_code=403, detail="you can cancel only your own return order")

    if return_order.status != "pending":
        raise HTTPException(status_code=400, detail=f"return order cannot be canceled {return_order.status} status")
    
    db.delete(return_order)
    db.commit()

    return {
        "message" : " return order canceled successfully"
    }


