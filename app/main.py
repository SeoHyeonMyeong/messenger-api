from fastapi import FastAPI, Response, status, HTTPException, Depends
from model import models
from model.models import Message
from model.schemas import MessageCreate
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# [GET] Root
@app.get("/")
def root():
    return {"message": "Hello World"}

# [POST] Create Message
@app.post("/messages", status_code=status.HTTP_201_CREATED)
def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    new_message = Message(**message.dict())
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    
    return {"data": new_message}

# [GET] Get Messages
@app.get("/messages")
def get_messages(db: Session = Depends(get_db)):
    messages = db.query(Message).all()
    return {"data": messages}

# [GET] Get Latest Message
@app.get("/messages/latest")
def get_latest_message(db: Session = Depends(get_db)):
    message = db.query(Message).order_by(Message.created_at).first()
    
    return {"data": message}

# [GET] Get Message
@app.get("/messages/{id}")
def get_message(id: int, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == id).first()
    if message == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"message with id: {id} was not found")
        
    return {"data": message}

# [PUT] Update Message
@app.put("/messages/{id}")
def update_message(id: int, updated_message: MessageCreate, db: Session = Depends(get_db)):
    query = db.query(Message).filter(Message.id == id)
    message = query.first()
    
    if message == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"message with id: {id} was not found")

    query.update(updated_message.dict(), synchronize_session=False)
    db.commit()

    return {"data": query.first()}

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