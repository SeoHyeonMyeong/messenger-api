from pydantic import BaseModel
from datetime import datetime

class MessageBase(BaseModel):
    title: str
    content: str
    
class MessageCreate(MessageBase):
    pass

class MessageOut(MessageBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
        
        
class UserBase(BaseModel):
    email: str
    password: str
    name: str

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True