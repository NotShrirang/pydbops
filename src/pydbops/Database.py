from pydbops.pydbops import pydbops
from pydbops.tables import Table
from typing import overload


class Database(pydbops):
    """
    Class for database operations.

    Args :
        filepath (str): path for database file.
    """
    def __init__(self, filepath: str) -> None:
        super().__init__(filepath)
        self.__filepath = filepath
        self.tables = self.tableNames(count=False, list=True, dictionary=False)

    def __str__(self) -> str:
        string = ""
        for table in self.tables:
            t = Table(table=table, filepath=self.__filepath)
            if t.length() == 0:
                continue
            else:
                string = string + str(t)
        return str(string)

    def addEntry(self, table: str, values: dict[str, str]) -> int:
        """
        Function for inserting values in database.

        Args:
            table (str) : tablename.
            values (dict): key is field name and value is value to be inserted.

        Returns:
            id of the entry inserted.
        """
        return super().addEntry(table, values)

    def createTable(self, tableName: str, fields: dict[str, str]) -> bool:
        """
        Creates table of given name.

        Args:
            - tableName (str) : Name of table.
            - fields (dict) : Dictionary of (columns names : data types)
        Returns:
            - True if executed.
        """
        return super().createTable(tableName, fields)

    def databaseVersion(self) -> str:
        return super().databaseVersion()

    @overload
    def getFieldNames(self, table: str, returnType: str = "int") -> int: ...

    @overload
    def getFieldNames(self, table: str, returnType: str = "list") -> list[str]: ...

    def getFieldNames(self, table: str, returnType: str = "list") -> int | list[str]:
        return super().getFieldNames(table, returnType)

    def getTable(self, table: str) -> Table:
        """
        Creates Table instance.

        Args:
            table (str) : table name.

        Returns: Table
        """
        t = Table(table=table, filepath=self.__filepath)
        return t

    def length(self) -> int:
        return super().length()

    def removeEntry(self, table: str, id: int = -1, keyword: str = "", deleteAllOccurences: bool = False, deleteAll: bool = False) -> bool:
        return super().removeEntry(table, id, keyword, deleteAllOccurences, deleteAll)

    @overload
    def searchEntry(self, table: str, id: int = -1, keyword: str = "", returnType: str = "ids", findAllOccurence: bool = False) -> int: ...

    @overload
    def searchEntry(self, table: str, id: int = -1, keyword: str = "", returnType: str = "list", findAllOccurence: bool = True) -> list[tuple[int | str]]: ...

    def searchEntry(self, table: str, id: int = -1, keyword: str = "", returnType: str = "ids", findAllOccurence: bool = False) -> int | list[tuple[int | str]]:
        return super().searchEntry(table, id, keyword, returnType, findAllOccurence)

    @overload
    def tableNames(self, count: bool = True, list: bool = False, dictionary: bool = False) -> int: ...

    @overload
    def tableNames(self, count: bool = False, list: bool = True, dictionary: bool = False) -> list[str]: ...

    @overload
    def tableNames(self, count: bool = False, list: bool = False, dictionary: bool = True) -> dict[str, str]: ...

    def tableNames(self, count: bool = False, list: bool = True, dictionary: bool = False) -> int | list[str] | dict[str, str]:
        return super().tableNames(count, list, dictionary)

    @overload
    def updateEntry(self, table: str, values: dict[str, str | int], field: str, whereFieldIs: int) -> bool: ...

    @overload
    def updateEntry(self, table: str, values: dict[str, str | int], field: str, whereFieldIs: str) -> bool: ...

    def updateEntry(self, table: str, values: dict[str, str | int], field: str, whereFieldIs: str | int) -> bool:
        return super().updateEntry(table, values, field, whereFieldIs)


def openDatabase(filename: str) -> Database:
    """
    Creates a database and returns a Database object.
    """
    d = Database(filepath=filename)
    return d
