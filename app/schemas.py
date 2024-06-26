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
    id: Optional[int] = None
    created_at: datetime = None
    user_id: Optional[int] = None
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
    # class Config:  # Edited
    #     from_attributes = True
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    class Config:
        from_attributes = True
    
class TokenData(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    user_id: Optional[int] = None
    
class PostMeta(PostBase):   # This Return Post Data with Owner Meta data:
    user: UserOut    # Same for What relation you mapped in models.
    class Config:
        from_attributes = True