from fastapi import FastAPI, Response, status, HTTPException
from model.Message import Message
import itertools

app = FastAPI()
messages = dict()
id_counter = itertools.count(1)

m = Message(title="Hi",content="Hello").dict()
id = next(id_counter)
m['id'] = id
messages[id] = m
m = Message(title="Nice to meet you!", content="...").dict()
id = next(id_counter)
m['id'] = id
messages[id] = m
print(messages.values())

# 우선순위는 위에 있는 함수!
@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/messages", status_code=status.HTTP_201_CREATED)
def create_message(message: Message):
    m = message.dict()
    id = next(id_counter)
    m['id'] = id
    messages[id] = m
    return {"success": "True"}


@app.get("/messages")
def list_messages():
    return {"data": list(messages.values())}


@app.get("/messages/latest")
def get_latest_message():
    m = list(messages.values())[-1]
    return {"message": m}


@app.get("/messages/{id}")
def get_message(id: int, response: Response):
    if not id in messages:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"message with id: {id} was not found")
    message = messages[id]
    return {"message": message}


@app.put("/messages/{id}")
def update_message(id: int, message: Message):
    if not id in messages:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"message with id: {id} was not found")
    messages[id] = message
    return {"success": "True"}


@app.delete("/messages/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_message(id: int):
    if not id in messages:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"message with id: {id} was not found")
    del(messages[id])
    return Response(status_code=status.HTTP_204_NO_CONTENT)