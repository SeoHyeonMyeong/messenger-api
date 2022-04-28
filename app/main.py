from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from . import models, schemas
from .models import Message
from .schemas import MessageCreate
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# [GET] Root
@app.get("/")
def root():
    return {"message": "Hello World"}

# [POST] Create Message
@app.post("/messages", response_model=schemas.Message)
def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    new_message = Message(**message.dict())
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    
    return new_message

# [GET] Get Messages
@app.get("/messages", response_model=List[schemas.Message])
def get_messages(db: Session = Depends(get_db)):
    messages = db.query(Message).all()
    return messages

# [GET] Get Latest Message
@app.get("/messages/latest", response_model=schemas.Message)
def get_latest_message(db: Session = Depends(get_db)):
    message = db.query(Message).order_by(Message.created_at).first()
    
    return message

# [GET] Get Message
@app.get("/messages/{id}", response_model=schemas.Message)
def get_message(id: int, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == id).first()
    if message == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"message with id: {id} was not found")
        
    return message

# [PUT] Update Message
@app.put("/messages/{id}", response_model=schemas.Message)
def update_message(id: int, updated_message: MessageCreate, db: Session = Depends(get_db)):
    query = db.query(Message).filter(Message.id == id)
    message = query.first()
    
    if message == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"message with id: {id} was not found")

    query.update(updated_message.dict(), synchronize_session=False)
    db.commit()

    return query.first()

# [DELETE] Delete Message
@app.delete("/messages/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_message(id: int, db: Session = Depends(get_db)):
    
    query = db.query(Message).filter(Message.id == id)
    
    if query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"message with id: {id} was not found")
    
    query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)