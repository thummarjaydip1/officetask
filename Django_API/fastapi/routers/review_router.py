from fastapi import APIRouter, Depends, HTTPException, Form, Request
from sqlalchemy.orm import Session

from database.database import get_db
from models.model import Product, Review, User
from auth import get_current_user

router = APIRouter(
    prefix="/reviews",
    tags = ["Reviews"]
)


# http://127.0.0.1:8000/reviews/add
@router.post("/add")
def add_review(
    product_id : int = Form(...),
    message : str = Form(...),
    user_id : int = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    review = db.query(Review).filter(
        Review.product_id == product.id,
        Review.user_id == user_id
    ).first()

    if review:
        raise HTTPException(status_code=400, detail="Product review sended already you can update own review")
    
    new_review = Review(
        user_id = user_id,
        product_id = product.id,
        message = message
    )

    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return {
        "msg": "Review send successfully",
        "id" : new_review.id,
        "product_name" : product.name,
        "message" : message
    }


# http://127.0.0.1:8000/reviews/display
@router.get("/display")
def display_review(
    request : Request,
    db : Session = Depends(get_db)
):
    reviews = db.query(Review).all()

    data = []

    for review in reviews:

        user = db.query(User).filter(User.id == review.user_id).first()
        product = db.query(Product).filter(Product.id == review.product_id).first()

        data.append({
            "id" : review.id,
            "product_name" : product.name,
            "image" : str(request.base_url) + f"media/product/{product.image}",
            "message" : review.message,
            "username" : user.username
        })
    
    return data


# http://127.0.0.1:8000/reviews/my-review
@router.get("/my-reviews")
def display_my_review(
    request : Request,
    user_id : int = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    reviews = db.query(Review).filter(Review.user_id == user_id).all()

    data = []

    for review in reviews:

        user = db.query(User).filter(User.id == review.user_id).first()
        product = db.query(Product).filter(Product.id == review.product_id).first()

        data.append({
            "id" : review.id,
            "product_name" : product.name,
            "image" : str(request.base_url) + f"media/product/{product.image}",
            "message" : review.message,
            "username" : user.username
        })

    return data


# http://127.0.0.1:8000/reviews/update/{id}
@router.put("/update/{id}")
def update_review(
    id : int,
    message : str = Form(...),
    user_id : int = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    data = db.query(Review).filter(Review.id == id).first()

    if not data:
        raise HTTPException(status_code=404, detail="Review not found")
    
    if data.user_id != user_id:
        raise HTTPException(status_code=400, detail="you can update only own review please check your review id")
    
    data.message = message
    db.commit()

    return {
        "message" : "Review Updated Successfully"
    }


# http://127.0.0.1:8000/reviews/delete/{id}
@router.delete("/delete/{id}")
def delete_review(
    id : int,
    user_id : int = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    data = db.query(Review).filter(Review.id == id).first()

    if not data:
        raise HTTPException(status_code=404, detail="Review not found")

    if data.user_id != user_id:
        raise HTTPException(status_code=400, detail="You can delete only own reviews")
    
    db.delete(data)
    db.commit()

    return {
        "message" : "Review Delete Successfully"
    }


# http://127.0.0.1:8000/reviews/count
@router.get("/count")
def count_review(
    db : Session = Depends(get_db)
):
    total_reviews = db.query(Review).count()
    
    return {
        "total_reviews" : total_reviews
    }