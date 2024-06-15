from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, conint

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
    class Config:
        from_attributes = True
        
class CreatePost(PostBase):
    pass

class SpecificUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None
    
    class Config:
        from_attributes = True

class PostResponse(PostBase):
    created_at: datetime = None
    class Config:
        from_attributes = True
        
class CreateUser(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    created_at: datetime