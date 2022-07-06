from DatabaseOperations import Database

def openDatabase(filename:str):
    """
    Creates a database and returns a Database object.
    """
    d = Database(filepath=filename)
    return d