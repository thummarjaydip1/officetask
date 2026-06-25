from fastapi import FastAPI

from database.database import Base, engine

from routers.bill_router import router as bill_router 

from routers.notification_router import router as notification_router

app = FastAPI(
    title="WEBHOOK WITH FASTAPI"
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return "WEB Hook"


app.include_router(bill_router)

app.include_router(notification_router)