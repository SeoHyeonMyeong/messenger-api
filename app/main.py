from fastapi import FastAPI, Response, status, HTTPException
from model.Message import Message
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# DB 연결
while True:
    try:
        conn = psycopg2.connect(host='localhost',
                                database='messenger', 
                                user='postgres', 
                                password='password',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connecting to database Failed!")
        print("Error: ", error)
        time.sleep(2)

# 우선순위는 위에 있는 함수!
# [GET] Root
@app.get("/")
def root():
    return {"message": "Hello World"}

# [POST] Create Message
@app.post("/messages", status_code=status.HTTP_201_CREATED)
def create_message(message: Message):
    
    cursor.execute("""INSERT INTO messages (title, content) VALUES (%s,%s) RETURNING * """,
                   (message.title, message.content))
    message = cursor.fetchone()
    conn.commit()
    
    return {"data": message}

# [GET] List Messages
@app.get("/messages")
def list_messages():
    
    cursor.execute("""SELECT * FROM messages;""")
    messages = cursor.fetchall()
    
    return {"data": messages}

# [GET] Get Latest Message
@app.get("/messages/latest")
def get_latest_message():
    
    cursor.execute("""SELECT * FROM messages ORDER BY created_at DESC LIMIT 1""")
    message = cursor.fetchone()
    
    return {"data": message}

# [GET] Get Message
@app.get("/messages/{id}")
def get_message(id: int):
    
    cursor.execute("""SELECT * FROM messages WHERE id = %s""",(str(id)))
    message = cursor.fetchone()
    
    if message == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"message with id: {id} was not found")
        
    return {"data": message}

# [PUT] Update Message
@app.put("/messages/{id}")
def update_message(id: int, message: Message):
    
    cursor.execute("""UPDATE messages SET title = %s, content = %s WHERE id = %sRETURNING *""",
                   (message.title, message.content, str(id),))
    message = cursor.fetchone()
    conn.commit()
    
    if message == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"message with id: {id} was not found")

    return {"data": message}

# [DELETE] Delete Message
@app.delete("/messages/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_message(id: int):
    
    cursor.execute("""DELETE FROM messages WHERE id = %s RETURNING * """, (str(id),))
    message = cursor.fetchone()
    conn.commit()
    
    if message == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"message with id: {id} was not found")
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)