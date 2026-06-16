from fastapi import APIRouter, HTTPException, Depends, Form, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database.database import SessionLocal
from models.model import Order,Product, User
from jose import jwt

router = APIRouter(
    prefix = "/orders",
    tags = ["Order"]
)

oauth2_schemas = OAuth2PasswordBearer(tokenUrl="/users/login")

SECREATE_KEY = "my_screate_key_with_jwt_project_with_fast_api"
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

        
@router.post("/add")
def add_order(
    product_name: str = Form(...),
    token: str = Depends(oauth2_schemas),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECREATE_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid User")
        
        product = db.query(Product).filter(Product.name == product_name).first()

        if not product:
            return {"message":"Product Not Found Plaese Enter Correct Product Name"}

        new_order = Order(
            user_id = user_id,
            product_id = product.id
        )

        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        return {
            "message" : "Place Order Successfully",
            "order_id": new_order.id
        }

    except:
        raise HTTPException(status_code=400, detail="Please Login Agains...")


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
            "address" : user.address
        })

    return data


@router.get("/pagination/display")
def pagination_display_order(
    request : Request,
    page : int = 1,
    size : int = 3,
    db : Session = Depends(get_db)
):
    total = db.query(Order).count()

    orders = db.query(Order).offset((page - 1) * size).limit(size).all()
    new = db.query(Order).offset((page-1)*size).limit(size).all()
    
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


@router.put("/update/{id}")
def update_order(
    id: int,
    product_name: str = Form(...),
    token: str = Depends(oauth2_schemas),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECREATE_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid User")

        order = db.query(Order).get(id)

        if not order:
            raise HTTPException(status_code=404, detail="Order Not Found")

        product = db.query(Product).filter(Product.name == product_name).first()
        
        order.user_id = user_id
        order.product_id = product.id
        
        db.commit()
        db.refresh(order)

        return {
            "message" : "Order Update Successfully",
            "order_id" : order.id
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail="Please Login Again...")


@router.delete("/delete/{id}")
def delete_order(
    id: int,
    token: str = Depends(oauth2_schemas),
    db: Session = Depends(get_db)    
):
    try:
        payload = jwt.decode(token, SECREATE_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid User")
        
        data = db.query(Order).get(id)

        if not data: 
            return {"message": "Order Not Found"}
 
        db.delete(data)
        db.commit()

        return {"message" : "Order Deleted Successfully"}

    except:
        raise HTTPException(status_code=400, detail="Please Login Again...")
    
@router.get("/search")
def search_order(
    request : Request,
    product_name : str = None,
    db : Session = Depends(get_db)
):
    products = db.query(Product).filter(
        Product.name.contains(product_name)
    ).first()

    if not products:
        raise HTTPException(status_code=404, detail="Product not found")
    
    orders = db.query(Order).filter(
        Order.product_id == products.id
    ).all()

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
            "Delivary_Address" : user.address
        })
    
    return data
