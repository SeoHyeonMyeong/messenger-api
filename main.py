from fastapi import Body, FastAPI
from model.Message import Message

app = FastAPI()
m = []
# 우선순위는 위에 있는 함수!
@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/send")
def send_message(payload: dict = Body(...)):
    m.append(Message(payload))
    return {"success": "True"}

@app.get("/list")
def list_message():
    list = [item.get_data() for item in m]
    return {"data": list}