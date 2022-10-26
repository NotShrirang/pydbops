from pydbops import *
from platforms_names import *
def openDatabase(system: str, filename: str, username: str = "", password: str = "") -> Database:
    """
    Creates a database and returns a Database object.
    """
    if system == SQLITE:
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
        
    elif system == MYSQL:
        mydb = mysql.connector.connect(
            host = "localhost",
            user = username,
            password = password
        )

