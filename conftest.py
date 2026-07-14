import pytest
from app import PyFremioApp

@pytest.fixture
def app():
    return PyFremioApp()

@pytest.fixture
def test_client(app):
    return app.test_session()