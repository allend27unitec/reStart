from typing import List, Dict
import sys
sys.path.append("../../01Assignment")
from Part_2 import main, message_model, Message, MessageUpdateRequest
from uuid import UUID
import pytest

@pytest.mark.asyncio
async def test_get_messages():
    db = await main.get_all_messages()
    for message in db:
        assert isinstance(message, Message)
        assert message.id is not None
        assert isinstance(message.id, UUID)
        assert message.to_address is not None
        assert isinstance(message.to_address, str)
        assert message.from_address is not None
        assert isinstance(message.from_address, str)
        assert message.subject is not None
        assert isinstance(message.subject, str)
        assert message.text is not None
        assert isinstance(message.text, str)


