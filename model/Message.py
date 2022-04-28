from pydantic import BaseModel

class Message(BaseModel):
    title: str
    content: str
    validation: bool = True