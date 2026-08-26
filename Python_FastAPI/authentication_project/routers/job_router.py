from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from models.model import *
from databases.database import get_db
from auth import get_user

router = APIRouter(
    prefix="/jobs",
    tags=['Job']
)


@router.post("/apply")
def apply_job(
    subject : str = Form(...),
    company_id : int = Form(...),
    user_id : int = Depends(get_user),
    db : Session = Depends(get_db)
):
    new_job = Job(
        subject = subject,
        user_id = user_id,
        company_id = company_id
    )
    db.add(new_job)
    db.commit()
    return {
        "message" : "Job Apply Successfully",
        "id" : new_job.id
    }


@router.get("/list")
def list_jobs(
    db: Session = Depends(get_db)
):
    jobs = db.query(Job).all()
    data = []

    for job in jobs:

        user = db.query(User).filter(User.id == job.user_id).first()
        company = db.query(Company).filter(Company.id == job.company_id).first()

        data.append({
            "id" : job.id,
            "subject" : job.subject,
            "comapany_name" : company.name,
            "company_owner_name" : company.owner_name,
            "username" : user.username,
            "email" : user.email,
            "address" : user.address
        })

    return data


@router.get("/user")
def user_jobs(
    user_id : int = Depends(get_user),
    db : Session = Depends(get_db)
):
    jobs = db.query(Job).filter(Job.user_id == user_id).all()
    data = []

    user = db.query(User).filter(User.id == user_id).first()

    for job in jobs:
        company = db.query(Company).filter(Company.id == job.company_id).first()

        data.append({
            "id" : job.id,
            "subject" : job.subject,
            "copany_name" : company.name,
            "company_owner_name" : company.owner_name,
            "username" : user.username,
            "email" : user.email,
            "address" : user.address
        })

    return data


@router.put("/update/{id}")
def update_job(
    id : int,
    user_id : int = Depends(get_user),
    subject : str = Form(None),
    company_id : int = Form(None),
    db : Session = Depends(get_db)
):
    job = db.query(Job).filter(Job.id == id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    user = db.query(User).filter(User.id == user_id).first()

    if user.id != job.user_id:
        raise HTTPException(status_code=404, detail="please update in own record")

    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="company not found")

    job.subject = subject
    job.company_id = company_id

    db.commit()
    return {
        "message" : "Job updated successfully",
        "id" : job.id
    }


@router.delete("/delete/{id}")
def delete_job(
    id : int,
    user_id : int = Depends(get_user),
    db : Session = Depends(get_db)
):
    data = db.query(Job).filter(Job.id == id).first()
    if not data:
        raise HTTPException(status_code=404, detail="job not found")

    if data.user_id != user_id:
        raise HTTPException(status_code=404, detail="please delete in own record")

    db.delete(data)
    db.commit()
    return {
        "message" : "job deleted successfully"
    }

