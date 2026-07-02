from fastapi import APIRouter, HTTPException, Depends, Form, Request
from sqlalchemy.orm import Session

from database.database import get_db
from models.model import *
from auth import get_current_user

router = APIRouter(
    prefix = "/carts",
    tags = ["Cart"]
)


# http://127.0.0.1:8000/carts/add
@router.post("/add")
def add_cart(
    product_id : int = Form(...),
    quantity : int = Form(...),
    user_id : int = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Enter more than 0(zero) qunatity")
    
    cart = db.query(Cart).filter(
        Cart.product_id == product.id,
        Cart.user_id == user_id
    ).first()

    if cart:
        raise HTTPException(status_code=409, detail="Product is already exists in own cart than you can update cart")

    total_price = quantity * int(product.price)

    new_cart = Cart(
        user_id = user_id,
        product_id = product.id,
        quantity = quantity,
        total = total_price
    )

    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)

    return {
        "message": "Product added to cart successfully",
        "cart_id": new_cart.id,
        "product_name": product.name,
        "quantity": new_cart.quantity,
        "total": new_cart.total
    }
    

# http://127.0.0.1:8000/carts/my-cart
@router.get("/my-carts")
def display_my_cart(
    request : Request,
    user_id : int = Depends(get_current_user),
    db : Session = Depends(get_db)
):  
    carts = db.query(Cart).filter(Cart.user_id == user_id).all()

    if not carts:
        raise HTTPException(status_code=404, detail="Cart product not found")

    data = []

    for cart in carts:

        product = db.query(Product).filter(Product.id == cart.product_id).first()
        user = db.query(User).filter(User.id == cart.user_id).first()

        data.append({
            "id" : cart.id,
            "product_name" : product.name,
            "product_price" : product.price,
            "product_image" : str(request.base_url) + f"media/product/{product.image}",
            "quantity" : cart.quantity,
            "total_price" : cart.total,
            "username" : user.username
        })
    
    return data


# http://127.0.0.1:8000/carts/update/{id}
@router.put("/update/{id}")
def update_cart(
    id: int,
    quantity : int = Form(...),
    user_id : int = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    data = db.query(Cart).get(id)

    if not data:
        raise HTTPException(status_code=404, detail="cart product not found")
    
    product = db.query(Product).filter(Product.id == data.product_id).first()

    if data.user_id != user_id:
        raise HTTPException(status_code=404, detail="you can update own cart product please check your cart product id")
    
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Enter more than 0(zero) qunatity")
    
    total_price = quantity * int(product.price)

    data.quantity = quantity
    data.total = total_price

    db.commit()
    db.refresh(data)

    return {
        "message" : "Cart product updated Successfully",
        "updated_qty" : data.quantity,
        "updated_total" : data.total
    }
    

# http://127.0.0.1:8000/carts/delete/{id}
@router.delete("/delete/{id}")
def delete_cart(
    id : int,
    user_id : int = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    data = db.query(Cart).get(id)

    if not data:
        raise HTTPException(status_code=404, detail="Cart Product not found")
    
    if data.user_id != user_id:
        raise HTTPException(status_code=404, detail="you can delete own cart product please check your cart product id")
    
    db.delete(data)
    db.commit()
    
    return {
        "message" : "Cart Product Delete Successfully"
    }


# http://127.0.0.1:8000/carts/search
@router.get("/search")
def search_cart(
    request : Request,
    product_name : str = None,
    user_id : int = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    product = db.query(Product).filter(Product.name == product_name).first()

    if not product:
        raise HTTPException(status_code=404, detail="Cart product not found")
    
    carts = db.query(Cart).filter(
        Cart.product_id == product.id,
        Cart.user_id == user_id
    ).all()

    if not carts:
        raise HTTPException(status_code=404, detail="please check your cart product not found")

    data = []

    for cart in carts:
        data.append({
            "id" : cart.id,
            "product_name" : product.name,
            "product_price" : product.price,
            "product_image" : str(request.base_url) + f"media/product/{product.image}",
            "quantity" : cart.quantity,
            "total_price" : cart.total,
            "username" : user.username
        })
    
    return data
