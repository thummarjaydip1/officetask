from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from schemas.bill_schema import BillSchemas, BillSchemasUpdate
from models.model import Bill

router = APIRouter(
    prefix = "/webhook",
    tags = ["Bill"]
)

@router.post("/bill/add")
def webhook_bill_add(
    data : BillSchemas,
    db : Session = Depends(get_db)
):
    new_bill = Bill(
        order_id = data.order_id,
        customer_name = data.customer_name,
        product_name = data.product_name,
        price = data.price,
        quantity = data.quantity,
        total_price = data.total_price
    )
    
    db.add(new_bill)
    db.commit()
    db.refresh(new_bill)

    return {
        'message' : "webhook bill receive successfully",
        "bill_id" : new_bill.id
    }


@router.get("/bill/display")
def webhook_bill_display(
    db : Session = Depends(get_db)
):
    bills = db.query(Bill).all()

    data = []

    for bill in bills:

        data.append({
            "id" : bill.id,
            "customer_name" : bill.customer_name,
            "product_name" : bill.product_name,
            "price" : bill.price,
            "quantity" : bill.quantity,
            "total_price" : bill.total_price
        })

    return data


@router.put("/bill/update/{id}")
def webhook_bill_update(
    id : int,
    data : BillSchemasUpdate,
    db : Session = Depends(get_db)
):
    bill = db.query(Bill).filter(Bill.order_id == id).first()

    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    bill.quantity = data.quantity
    bill.total_price = data.total_price

    db.commit()
    db.refresh(bill)

    return {
        "message" : "Bill Updated Successfully"
    }
    

@router.delete("/bill/delete/{id}")
def webhook_bill_delete(
    id : int,
    db : Session = Depends(get_db)
):
    
    data = db.query(Bill).filter(Bill.order_id == id).first()

    if not data:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    db.delete(data)
    db.commit()

    return {
        "message" : "Bill Deleted Successfully"
    }
