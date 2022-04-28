from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from . import models, schemas
from .models import Message, User
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# [GET] Root
@app.get("/")
def root():
    return {"message": "Hello World"}

# [POST] Create Message
@app.post("/messages", response_model=schemas.MessageOut)
def create_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    new_message = Message(**message.dict())
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    
    return new_message

# [GET] Get Messages
@app.get("/messages", response_model=List[schemas.MessageOut])
def get_messages(db: Session = Depends(get_db)):
    messages = db.query(Message).all()
    return messages

# [GET] Get Latest Message
@app.get("/messages/latest", response_model=schemas.MessageOut)
def get_latest_message(db: Session = Depends(get_db)):
    message = db.query(Message).order_by(Message.created_at).first()
    
    return message

# [GET] Get Message
@app.get("/messages/{id}", response_model=schemas.MessageOut)
def get_message(id: int, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == id).first()
    if message == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"message with id: {id} was not found")
        
    return message

# [PUT] Update Message
@app.put("/messages/{id}", response_model=schemas.MessageOut)
def update_message(id: int, updated_message: schemas.MessageCreate, db: Session = Depends(get_db)):
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

# [POST] Create User
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

# [GET] Get Users
@app.get("/users", response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    
    return users

# [GET] Get User
@app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} was not found")

    return user


# [DELETE] Delete User
@app.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id:int, db: Session = Depends(get_db)):
    query = db.query(User).filter(User.id == id)
    
    if query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} was not found")
        
    query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)