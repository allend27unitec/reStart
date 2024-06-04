from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

class Message(BaseModel):
    id: int 
    to_address: str
    from_address: str
    copy_to: Optional[str]
    subject: Optional[str]
    text: Optional[str]
    attachment: Optional[str]

class MessageUpdateRequest(BaseModel):
    to_address: str
    from_address: str
    copy_to: Optional[str]
    subject: Optional[str]
    text: Optional[str]
    attachment: Optional[str]
