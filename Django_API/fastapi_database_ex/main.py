from fastapi import FastAPI
from routers.contact_router import router as contact_router
from routers.feedback_router import router as feedback_router

app = FastAPI()

@app.get('/')
def home():
    return {"message":"Contact & Feedback API Project With Database"}

app.include_router(contact_router)
app.include_router(feedback_router)