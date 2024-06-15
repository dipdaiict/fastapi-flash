from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

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