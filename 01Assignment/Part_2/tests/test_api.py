import sys
sys.path.append("../")
from schemas.message_model import Message 
from main import app
from fastapi.testclient import TestClient
import pytest
from typing import List
import requests
import logging

API_URL = "http://localhost:8000"

@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    yield client
    
def test_url():
    response = requests.get(API_URL)
    assert response.status_code == 200

def test_get_all_messages(test_client, caplog):
    with caplog.at_level(logging.INFO):
        response = test_client.get("/api/get_messages")
        assert response.status_code == 200

    db:List = response.json()
    #db = Message(**db).model_dump(mode='json')
    for msg in db:
        msg1 = Message(**msg)
        assert isinstance(msg1, Message)
        assert msg1.id is not None
        assert isinstance(msg1.id, int)
        assert msg1.from_address != ""
        assert isinstance(msg1.from_address, str)
        assert msg1.to_address != ""
        assert isinstance(msg1.to_address, str)
        assert msg1.subject != ""
        assert isinstance(msg1.subject, str)

def test_create_message(test_client, caplog):
    with caplog.at_level(logging.INFO):
        payload = {
            'id':1,
            'from_address':"dca@gmail.com",
            'to_address':"dca@gmail.com",
            'copy_to':"",
            'subject':"Subject",
            'text':"Text",
            'attachment':"please find attached"
        }

        response = test_client.post("/api/create/", json=payload)
        assert response.status_code == 201
        employee = Message.model_validate(response.json())
        assert employee.from_address == "dca@gmail.com"
        assert "Auto-incrementing - new id is 4" in caplog.text

def test_delete_message(test_client, caplog):
    payload = {
        'id':6,
        'from_address':"dca@gmail.com",
        'to_address':"dca@gmail.com",
        'copy_to':"",
        'subject':"Subject",
        'text':"Text",
        'attachment':"please find attached"
    }
    response = test_client.post(f"/api/create/", json=payload)
    assert response.status_code == 201
    with caplog.at_level(logging.INFO):
        payload = 6
        response = test_client.delete(f"{API_URL}/api/delete/{payload}")
        assert "successful attempt to delete message 6" in caplog.text
        assert response.status_code == 204
        payload = 6
        response = test_client.delete(f"{API_URL}/api/delete/{payload}")
        assert "attempt to delete message 6 - not found" in caplog.text
        assert response.status_code == 404

def test_get_specific_message(test_client, caplog):
    with caplog.at_level(logging.INFO):
        payload = 2
        response = test_client.get(f"{API_URL}/api/get/{payload}")
        assert "message 2 not found" not in caplog.text
        assert response.status_code == 200


def test_patch_message(test_client, caplog):
    pass
    
