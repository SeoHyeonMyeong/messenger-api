from pydantic import BaseModel

class MessageBase(BaseModel):
    title: str
    content: str
    
class MessageCreate(MessageBase):
    pass