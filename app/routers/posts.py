from .. import oauth2
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from .. database import engine, get_db
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Response, HTTPException, status, Depends, APIRouter

router = APIRouter(tags=['POSTS'])  

@router.get("/posts")
def get_all_data(db: Session = Depends(get_db)):
    # print(db.query(models.Post))  # To See Which Query Executed behind the Backend.
    all_posts = db.query(models.Post).all()
    return all_posts

@router.post("/create_post", status_code= status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(posts: schemas.CreatePost, db: Session = Depends(get_db), 
                current_user = Depends(oauth2.get_current_user)):  
    # if posts. != current_user.username:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to Perform This Operation.")
    new_post = models.Post(title = posts.title, content=posts.content, published=posts.published)    # new_post = models.Post(**posts.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/posts/{id}", response_model=schemas.PostResponse)
def get_posts(id: int, response: Response, db: Session = Depends(get_db),
              current_user = Depends(oauth2.get_current_user)):
    post_info = db.query(models.Post).filter(models.Post.id == id).first()
    if not post_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id: {id} was Not Found....") 
    return post_info

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user = Depends(oauth2.get_current_user)):
    post_to_delete = db.query(models.Post).filter(models.Post.id == id).first() 
    if post_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID: {id} not found.")
    db.delete(post_to_delete)
    db.commit()
    return JSONResponse(content={"message": "Post successfully deleted."})

# Update The Post by ID:
@router.put("/posts/{id}")
def update_post(id: int, updated_post: schemas.CreatePost,  db: Session = Depends(get_db),
                current_user = Depends(oauth2.get_current_user)):
    post= db.query(models.Post).filter(models.Post.id == id)
    post_to_update = post.first()
    if post_to_update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=F"Post with ID: {id} Not Found.")
    post.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post.first()

# Specific Part Update:
@router.put("/posts/specific/{id}", response_model=schemas.PostBase)
def update_post_(id: int, updated_post: schemas.SpecificUpdate, db: Session = Depends(get_db), 
                 current_user = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID: {id} not found")
    for field, value in updated_post.dict(exclude_unset=True).items():
        setattr(post, field, value)
    db.commit()
    db.refresh(post)
    return post