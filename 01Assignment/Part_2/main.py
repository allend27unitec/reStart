from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
from uuid import UUID, uuid4
from .message_model import Message, MessageUpdateRequest

app = FastAPI()

db: List[Message] = [
    Message(
    id=UUID("34991cf7-5b4d-4bb4-977c-2253cd69a2b0"),
    from_address="jam@gmail.com",
    to_address="Ahmed@unitec.ac.nz",
    copy_to="",
    subject="Lorem ipsum",
    text="Lorem ipsum dolor sit amet, qui minim labore adipisicing minim sint cillum sint consectetur cupidatat.",
    attachment=""
    ),
    Message(
    id=UUID("b11b61d1-537f-469d-aa7a-11617e028506"),
    from_address="Fran@unitec.ac.nz",
    to_address="Ahmed@unitec.ac.nz",
    copy_to="",
    subject="This is the subject of the message",
    text="This is the text of the message",
    attachment="file://thisherefile.txt"
    ),
    Message(
    id=UUID("b90c04ce-16fc-4615-91d5-a39e3ebdd016"),
    from_address="dca@gamil.com",
    to_address="dca@gamil.com",
    copy_to="",
    subject="Subject",
    text="Text",
    attachment="please find attached"
    )]

@app.get("/")
async def get_all_messages() -> Dict:
    return db

@app.get("/api/get/{message_key}")
async def get_message(message_key: str) -> str:
    for message in db:
        if (id == message_key):
            return message

@app.post("/api/create")
async def create_message(message: Message):
    db.append(message)
    return {"new message id": message.id}

@app.delete("/api/delete/{message_id}")
async def delete_message(message_id: UUID):
    for message in db:
        if (message.id == message_id):
            db.remove(message)
            return {"deleted message": message_id} 
    raise HTTPException(
        status_code=404,
        detail=f"message with id: {message_id} does not exist"
        )

@app.patch("/api/update/{message_id}")
async def update_message(message_update: MessageUpdateRequest, message_id: UUID):
    for message in db:
        if (message.id == message_id):
            if (message_update.to_address is not None):
                message.to_address = message_update.to_address
            if (message_update.last_name is not None):
                message.from_address = message_update.from_address
            if (message_update.subject is not None):
                message.subject = message_update.subject
            if (message_update.text is not None):
                message.text = message_update.text
            if (message_update.copy_to is not None):
                message.copy_to = message_update.copy_to
            if (message_update.attachment is not None):
                message.attachment = message_update.attachment
            return
    raise HTTPException(
        status_code=404,
        detail=f"message with id: {message_id} does not exist"
        )
    return
