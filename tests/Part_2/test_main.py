from fastapi.testclient import TestClient
from .main import app
import pytest


@pytest.fixture
def client():
    yield TestClient(app)


def test_sample(client):
    assert True


# ========================================================================
#                 _                                _
#                | |                              | |
#    ___ ___   __| | ___    __ _  ___   ___  ___  | |__   ___ _ __ ___
#   / __/ _ \ / _` |/ _ \  / _` |/ _ \ / _ \/ __| | '_ \ / _ \ '__/ _ \
#  | (_| (_) | (_| |  __/ | (_| | (_) |  __/\__ \ | | | |  __/ | |  __/
#   \___\___/ \__,_|\___|  \__, |\___/ \___||___/ |_| |_|\___|_|  \___|
#                           __/ |
#                          |___/
# ========================================================================
