from fastapi import FastAPI
from .import models, utils
from .routers import posts, users, auth
from .database import engine, get_db

app = FastAPI()

models.Base.metadata.create_all(bind=engine)   # No Longer required after alembic setup first time used.
          
@app.get("/")  
def read_root():  
    return {"Message": "Welcome to the Home Page."} 

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)