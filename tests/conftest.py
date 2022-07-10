import pytest
from pydbops.Database import *

@pytest.fixture(scope="session")
def db_conn():
    db = openDatabase("MyDB.db")
    yield db