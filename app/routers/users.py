from sqlalchemy.orm import Session
from .. import models, schemas, utils
from .. database import engine, get_db
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Response, HTTPException, status, Depends, APIRouter

router = APIRouter(prefix="/user", tags=['USERS'])  

@router.post("/createuser", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def createuser(user: schemas.CreateUser, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password  # Update the hashed pass in pydantic data
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Retreive this newly created post and store with in new_post variable...
    return new_user

@router.get("/{username}", response_model=schemas.UserOut)
def user_data(username: str, db: Session = Depends(get_db)):
    user_data = db.query(models.User).filter(models.User.username == username).first()
    if user_data is None:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with username: {username} not found.")
    return user_data