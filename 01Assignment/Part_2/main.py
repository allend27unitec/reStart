from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List, Dict
import logging
from collections import Counter
from schemas.message_model import Message, MessageUpdateRequest

app = FastAPI(
    title="Assignment 1 Part 2 ",
    description="Demonstration of an (email) message API with logging (caplog)"
    )

logger=logging.getLogger('uvicorn')

# example of a dictionary database to satisfy 2.1
db1: List[Dict[str, Message]] = [{ 
    "message_1": Message(
    id=1,
    from_address="jam@gmail.com",
    to_address="Ahmed@unitec.ac.nz",
    copy_to="",
    subject="Lorem ipsum",
    text="Lorem ipsum dolor sit amet, qui minim labore adipisicing minim sint cillum sint consectetur cupidatat.",
    attachment=""
    )},{
    "message_2":Message(
    id=2,
    from_address="Fran@unitec.ac.nz",
    to_address="Ahmed@unitec.ac.nz",
    copy_to="",
    subject="This is the subject of the message",
    text="This is the text of the message",
    attachment="file://thisherefile.txt"
    )}]

db: List[Message] = [ 
    Message(
    id=1,
    from_address="jam@gmail.com",
    to_address="Ahmed@unitec.ac.nz",
    copy_to="",
    subject="Lorem ipsum",
    text="Lorem ipsum dolor sit amet, qui minim labore adipisicing minim sint cillum sint consectetur cupidatat.",
    attachment=""
    ),
    Message(
    id=2,
    from_address="Fran@unitec.ac.nz",
    to_address="Ahmed@unitec.ac.nz",
    copy_to="",
    subject="This is the subject of the message",
    text="This is the text of the message",
    attachment="file://thisherefile.txt"
    ),
    Message(
    id=3,
    from_address="dca@gamil.com",
    to_address="dca@gamil.com",
    copy_to="",
    subject="Subject",
    text="Text",
    attachment="please find attached"
    )]

db2: List[Message] = []

def check_message_exists(message_id:int) -> bool:
    for message in db:
        if (message.id == message_id):
            return True
    return False

@app.get("/")
async def root():
    return {"Hello": "Part 2"}

@app.get("/api/get_messages", status_code=status.HTTP_200_OK)
async def get_all_messages():
    cnt = Counter(getattr(Message, 'id') for Message in db)
    cnt = sum(cnt.values())
    logger.info(f"get all messages (count: {cnt})")
    if (cnt == 0):
        logger.error("no messages")
        raise HTTPException(
            status_code=404,
            detail=f"no messages"
            )
    else:
        return db

@app.get("/api/get/{message_id}", status_code=status.HTTP_200_OK, response_model=Message)
async def get_message(message_id: int):
    logger.info(f"attempt to find message with message_id {message_id}")
    for message in db:
        if (message.id == message_id):
            return message
    logger.error(f"message {message_id} not found")
    raise HTTPException(
        status_code=404,
        detail=f"message with id: {message_id} does not exist"
        )

@app.post("/api/create", status_code=status.HTTP_201_CREATED, response_model=Message)
async def create_message(message: Message):
    message_id = message.id
    if (check_message_exists(message_id)):
        cnt = Counter(getattr(Message, 'id') for Message in db)
        cnt = sum(cnt.values()) + 1
        logger.error(f"attempt to create message with id {message_id} - already exists.")
        logger.error(f"Auto-incrementing - new id is {cnt}")
        message.id = cnt
    db.append(message)
    return message

@app.delete("/api/delete/{message_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(message_id: int):
    for message in db:
        if (message.id == message_id):
            logger.info(f"successful attempt to delete message {message_id}")
            db.remove(message)
            return {f"deleted message: {message}"} 
    logger.error(f"attempt to delete message {message_id} - not found")
    raise HTTPException(
        status_code=404,
        detail=f"message with id: {message_id} does not exist"
        )

@app.patch("/api/update/{message_id}")
async def update_message(message_update: MessageUpdateRequest, message_id: int):
    for message in db:
        if (message.id == message_id):
            logger.info(f"old message {message}")
            if (message_update.to_address != ""):
                message.to_address = message_update.to_address
            if (message_update.from_address != ""):
                message.from_address = message_update.from_address
            if (message_update.subject != ""):
                message.subject = message_update.subject
            if (message_update.text != ""):
                message.text = message_update.text
            if (message_update.copy_to != ""):
                message.copy_to = message_update.copy_to
            if (message_update.attachment != ""):
                message.attachment = message_update.attachment
            logger.info(f"new message {message}")
            return message
    raise HTTPException(
        status_code=404,
        detail=f"message with id: {message_id} does not exist"
        )
