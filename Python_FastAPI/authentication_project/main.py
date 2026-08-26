from fastapi import FastAPI
from models.model import *
from databases.database import Base, engine
from routers.user_router import router as user_router
from routers.company_router import router as company_router
from routers.job_router import router as job_router

app = FastAPI()

# @app.get("/")
# def testing():
#     return "tesing api"

Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(company_router)
app.include_router(job_router)