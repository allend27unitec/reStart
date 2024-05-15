from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID, uuid4

app = FastAPI()

class Message(BaseModel):
    id: Optional[UUID] = uuid4()
    to_address: str
    from_address: str
    copy_to: Optional[str]
    subject: Optional[str]
    text: str
    attachment: Optional[str]

class MessageUpdateRequest(BaseModel):
    to_address: Optional[str]
    from_address: Optional[str]
    copy_to: Optional[str]
    subject: Optional[str]
    text: Optional[str]
    attachment: Optional[str]
