from fastapi import FastAPI
from .import models, utils
from .routers import posts, users, auth
from .database import engine, get_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "https://www.google.com",
    "https://accounts.google.com",
    "https://*.google.com"  # Allow all subdomains of google.com
]

# origins = ["*"]  # For Every Domain can requests.

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# models.Base.metadata.create_all(bind=engine)   # No Longer required after alembic setup first time used. Closed when pushing the code.
          
@app.get("/")  
def read_root():  
    return {"Message": "Welcome to the Home Page. Hey Buddy, Congratulations Dip Patel for Successfully Deployment."} 

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)