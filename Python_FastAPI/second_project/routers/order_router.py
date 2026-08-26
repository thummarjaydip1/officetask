from fastapi import APIRouter, Request, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from databases.database import get_db
from models.model import *

router = APIRouter(
    prefix="/orders",
    tags=["Order"]
)


@router.post("/add")
def add_order(
    quantity : int = Form(...),
    product_id : int = Form(...),
    db : Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    total_price = product.price * quantity

    new_order = Order(
        quantity = quantity,
        total_price = total_price,
        product_id = product.id
    )
    db.add(new_order)
    db.commit()
    return {
        "message" : "Order Place Successfully",
        "order_id" : new_order.id
    }


@router.get("/list")
def list_order(
    request : Request,
    db : Session = Depends(get_db)
):
    orders = db.query(Order).all()
    data = []

    for order in orders:
        product = db.query(Product).filter(Product.id == order.product_id).first()
        category = db.query(Category).filter(Category.id == product.category_id).first()

        data.append({
            "order_id" : order.id,
            "product_name" : product.name,
            "product_price" : product.price,
            "product_image" : str(request.base_url) + f"media/products/{product.image}",
            "quantity" : order.quantity,
            "total_price" : order.total_price,
            "category" : category.name
        })
    return data


@router.put("/update/{id}")
def update_order(
    id : int,
    quantity : int = Form(None),
    product_id : int = Form(None),
    db : Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail="order not found")

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    total_price = product.price * quantity

    order.quantity = quantity
    order.total_price = total_price
    order.product_id = product.id
    db.commit()

    return { 
        "message" : "Order Updated Successfully",
        "order_id" : order.id
    }

@router.delete("/delete/{id}")
def delete_order(
    id : int,
    db : Session = Depends(get_db)
):
    data = db.query(Order).filter(Order.id == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(data)
    db.commit()
    return {
        "message" : "Order Deleted Successfully"
    }