import psycopg2
from psycopg2 import OperationalError, Error
from psycopg2.extras import RealDictCursor
from enum import Enum
from random import randint
from typing import Optional, List
from pydantic import BaseModel
from fastapi.params import Body
from .database import engine, get_db
from .config import Settings
from fastapi import FastAPI, Response, HTTPException, status, Depends
from . import schemas, models
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
          
@app.get("/")  
def read_root():  
    return {"Message": "Welcome to the Home Page."} 

@app.get("/posts")
def get_all_data(db: Session = Depends(get_db)):
    # print(db.query(models.Post))  # To See Which Query Executed behind the Backend.
    all_posts = db.query(models.Post).all()
    return all_posts

@app.post("/create_post", status_code= status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(posts: schemas.CreatePost, db: Session = Depends(get_db)):  
    new_post = models.Post(title = posts.title, content=posts.content, published=posts.published)    # new_post = models.Post(**posts.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_posts(id: int, response: Response, db: Session = Depends(get_db)):
    post_info = db.query(models.Post).filter(models.Post.id == id).first()
    if not post_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id: {id} was Not Found....") 
    return post_info

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_to_delete = db.query(models.Post).filter(models.Post.id == id).first() 
    if post_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID: {id} not found.")
    db.delete(post_to_delete)
    db.commit()
    return JSONResponse(content={"message": "Post successfully deleted."})

# Update The Post by ID:
@app.put("/posts/{id}")
def update_post(id: int, updated_post: schemas.CreatePost,  db: Session = Depends(get_db)):
    post= db.query(models.Post).filter(models.Post.id == id)
    post_to_update = post.first()
    if post_to_update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=F"Post with ID: {id} Not Found.")
    post.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post.first()

# Specific Part Update:
@app.put("/posts/specific/{id}", response_model=schemas.PostBase)
def update_post_(id: int, updated_post: schemas.SpecificUpdate, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID: {id} not found")
    for field, value in updated_post.dict(exclude_unset=True).items():
        setattr(post, field, value)
    db.commit()
    db.refresh(post)
    return post