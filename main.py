from fastapi import FastAPI, Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from fastapi.testclient import TestClient


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/users/me")
async def read_user_me(token: str = Depends(oauth2_scheme)):
    return {"token": token}

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

def test_read_item():
    with TestClient(app) as client:
        response = client.get("/items/42")
        assert response.status_code == 200
        assert response.json() == {"item_id": 42, "query_param": None}

async def get_user_agent(user_agent: str = Header(None)):
    return {"User-Agent": user_agent}

@app.get("/user-agent/")
async def read_user_agent(user_agent: dict = Depends(get_user_agent)):
    return user_agent

@app.post("/items/")
def create_item(item: Item):
    return item

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, query_param: str = None):
    return {"item_id": item_id, "query_param": query_param}


