import pytest
from src.pydbops.database import *

@pytest.fixture(scope="session")
def db_conn() -> Database:
    db = openDatabase("MyDB.db")
    yield db