import pytest

from server import app


@pytest.fixture
def client():
    app.config.from_object(
        {
            "TESTING": True
        }
    )
    with app.test_client() as client:
        yield client