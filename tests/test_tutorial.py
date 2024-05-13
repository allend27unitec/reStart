import sys
sys.path.append("../")
from tutorial_models import UserAccount, Gender, Role, UserUpdateRequest
import tutorial
from uuid import UUID
import pytest

@pytest.mark.asyncio
async def test_fetch():
    db = await tutorial.fetch_users()
    for user in db:
        assert isinstance(user, UserAccount)
        assert user.id is not None
        assert isinstance(user.id, UUID)
        assert user.first_name is not None
        assert isinstance(user.first_name, str)
        assert user.last_name is not None
        assert isinstance(user.last_name, str)
        assert user.gender is not None
        assert isinstance(user.gender, Gender)
        assert user.roles is not None
        for role in user.roles:
            assert isinstance(role, Role)


