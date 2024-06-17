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
    print(f"Current User: {current_user.username} | Current User Email: {current_user.email}")
    new_post = models.Post(title = posts.title, content=posts.content, published=posts.published, user_id=current_user.user_id)    # new_post = models.Post(**posts.dict())
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
                current_user: models.User = Depends(oauth2.get_current_user)):
    post_to_delete = db.query(models.Post).filter(models.Post.id == id).first()
    if post_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID: {id} not found.")
    if post_to_delete.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete this post.")
    db.delete(post_to_delete)
    db.commit()
    return JSONResponse(content={"message": "Post successfully deleted."}, status_code=status.HTTP_204_NO_CONTENT)

# Update The Post by ID:
@router.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.CreatePost, db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_to_update = post_query.first()
    if post_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID: {id} not found.")
    if post_to_update.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post.")
    post_to_update.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(post_to_update)
    return post_to_update

# Specific Part Update:
@router.put("/posts/specific/{id}", response_model=schemas.PostBase)
def update_post_(id: int, updated_post: schemas.SpecificUpdate, db: Session = Depends(get_db), 
                 current_user = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_to_update = post_query.first()
    if post_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID: {id} not found.")
    if post_to_update.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post.")
    for field, value in updated_post.dict(exclude_unset=True).items():
        setattr(post_to_update, field, value)
    db.commit()
    db.refresh(post_to_update)
    return post_to_update