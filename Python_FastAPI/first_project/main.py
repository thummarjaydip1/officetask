from fastapi import FastAPI
from databases.database import Base, engine
from routers.router import router 

app = FastAPI()

@app.get("/")
def hello():
    return "hello"

Base.metadata.create_all(bind=engine)

app.include_router(router)