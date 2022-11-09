from pydbops import *
from pydbops.database import Database
import os
import mysql.connector
from pymongo import MongoClient

class Databases():
    SQLITE = 'sqlite3'
    MYSQL = 'mysql'
    POSTGRESQL = 'postgresql'
    MONGO = 'mongodb'
    FIREBASE = 'firebase'

def openDatabase(system: str, filename: str = "", username: str = "", password: str = "") -> Database:
    """
    Creates a database and returns a Database object.
    
    Args:

        - system: str = Database Management System name.
        - filename: str = Database file name for "SQLite"
        - username: str = Username for MySQL
        - password: str = Password for MySQL
    """
    if system == Databases.SQLITE:
        if filename[-3:] != ".db":
            raise(FileNotFoundError)

        index = filename.rfind("/")
        if not (index == -1):
            file_path = filename[index:]
            if not os.path.isdir(file_path):
                raise(FileNotFoundError)
        try:
            d = Database(filepath=filename)
            return d
        except FileNotFoundError:
            raise(FileNotFoundError(filename))
    
    elif system == Databases.MONGO:
        return MongoClient("mongodb://localhost:27017")

    elif system == Databases.MYSQL:
        mydb = mysql.connector.connect(
            host = "localhost",
            user = username,
            password = password
        )
        return mydb