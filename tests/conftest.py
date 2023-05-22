import os

import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "no_env_var: mark test to not use env var mock")


ENV_VARS = {
    key: f"test_{key.lower()}"
    for key in [
        "TGTG_ACCESS_TOKEN",
        "TGTG_REFRESH_TOKEN",
        "TGTG_USER_ID",
        "TGTG_COOKIE",
        "TGTG_TELEGRAMBOT_TOKEN",
        "TGTG_TELEGRAMBOT_CHAT_ID",
    ]
}


@pytest.fixture(autouse=True)
def mock_env_variables(request):
    if not request.node.get_closest_marker("no_profiling"):
        for env_var in ENV_VARS:
            os.environ[env_var] = ENV_VARS[env_var]
    yield


class TestClient:
    def __init__(self):
        pass

    def get_item(self, item_id):
        pass
