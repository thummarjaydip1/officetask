from fastapi import APIRouter, HTTPException, Depends, Form, Request
from sqlalchemy.orm import Session

from database.database import get_db
from models.model import *
from auth import get_current_user

router = APIRouter(
    prefix="/wishlists",
    tags=["Whishlist"]
)


# http://127.0.0.1:8000/wishlists/add
@router.post("/add")
def add_wishlist(
    product_id : int = Form(...),
    user_id : int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()
        
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    wish = db.query(Wishlist).filter(
        Wishlist.user_id == user_id,
        Wishlist.product_id == product.id
    ).first()
        
    if wish:
        raise HTTPException(status_code=409, detail="Product already exists in wishlist")
        
    wishlist = Wishlist(
        user_id = user_id,
        product_id = product.id
    )
    db.add(wishlist)
    db.commit()
    db.refresh(wishlist)

    return {
        "message" : "Product Adde to Wishlist",
        "id" : wishlist.id,
        "product_name" : product.name
    }

    
# http://127.0.0.1:8000/wishlists/my-wishlist
@router.get("/my-wishlists")
def display_my_wishlist(
    request : Request,
    user_id : int = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    wishlists = db.query(Wishlist).filter(Wishlist.user_id == user_id).all()

    data = []

    for wishlist in wishlists:

        user = db.query(User).filter(User.id == wishlist.user_id).first()

        product = db.query(Product).filter(Product.id == wishlist.product_id).first()
                                               
        data.append({
            "id" : wishlist.id,
            "product_name" : product.name,
            "product_price" : product.price,
            "product_image" : str(request.base_url) + f"media/product/{product.image}",
            "username" : user.username
        })
    
    return data

    
# http://127.0.0.1:8000/wishlists/delete/{id}
@router.delete("/delete/{id}")
def delete_wishlist(
    id : int, 
    user_id : int = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    data = db.query(Wishlist).get(id)
    # data = db.query(Wishlist).filter(Wishlist.id == id).first()

    if not data:
        raise HTTPException(status_code=404, detail="Wishlist item not found")

    if data.user_id != user_id:
        raise HTTPException(status_code=404, detail="you can delete own wishlist check your wishlist")
        
    db.delete(data)
    db.commit()
        
    return {
        "message" : "Product Remove Wishlist"
    }


# http://127.0.0.1:8000/wishlists/search
@router.get("/search")
def search_wishlist(
    request : Request,
    product_name : str = None,
    user_id : int = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    
    product = db.query(Product).filter(Product.name == product_name).first()

    if not product:
        raise HTTPException(status_code=404, detail="wishlist item not found")

    wishlist = db.query(Wishlist).filter(
        Wishlist.product_id == product.id,
        Wishlist.user_id == user_id 
    ).first()

    if not wishlist:
        raise HTTPException(status_code=404, detail="Product not found in own wishlist")
    
    data = []
    
    if wishlist:

        data.append({
            "id" : wishlist.id,
            "product_name" : product.name,
            "product_price" : product.price,
            "product_image" : str(request.base_url) + f"media/product/{product.image}",
            "username" : user.username
        })

    return data


# http://127.0.0.1:8000/wishlists/count
@router.get("/count")
def count_wishlist(
    db : Session = Depends(get_db)
):
    total_wishlist = db.query(Wishlist).count()
    
    return {
        "total_wishlists" : total_wishlist
    }