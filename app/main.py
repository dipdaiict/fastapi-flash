from fastapi import FastAPI
from .import models, utils
from .routers import posts, users
from .database import engine, get_db

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
          
@app.get("/")  
def read_root():  
    return {"Message": "Welcome to the Home Page."} 

app.include_router(posts.router)
app.include_router(users.router)