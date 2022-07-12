from pydbops.pydbops import pydbops
from pydbops.tables import Table
from typing import overload
from pydbops.UserDefinedExceptions import NoSuchTableError


class Database(pydbops):
    """
    Class for representing database

    Args:
    -----
        - filepath (str) : path to the database

    Methods:
    -------
        - addEntry() - Function for inserting values in table.
        - createTable() - Creates table of given name.
        - databaseVersion() - Returns sqlite3 version.
        - dropTable() - Function for deleting table.
        - fetchInOrder() - Function for fetching database entries in given order.
        - getFieldNames() - Function for getting field names.
        - length() - Returns length of table. Returns 0 if table is empty.
        - removeEntry() - Function for removing records from table.
        - searchEntry() - Function for searching in table.
        - tableNames() - Accesses tables in a database.
        - updateEntry() - Function for updating values in table.
        - values() - Accesses records in a table.
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
        ret = super().createTable(tableName, fields)
        self.tables = self.tableNames(count=False, list=True, dictionary=False)
        return ret

    def databaseVersion(self) -> str:
        """
        Returns sqlite3 version.
        """
        return super().databaseVersion()

    def dropTable(self, table: str, getData: bool = True) -> list[tuple[str | int, str | int, ]]:
        """
        Function for deleting table.

        Args:
            - table (str): Table name.
            - getData (bool): If True, returns all the data before deleting the table.

        Returns: list of records.
        """
        ret = super().dropTable(table=table, getData=getData)
        self.tables = self.tableNames(count=False, list=True, dictionary=False)
        return ret

    @overload
    def fetchInOrder(self, table: str, field: list[str]) -> list[tuple[str | int, str | int, ]]: ...

    @overload
    def fetchInOrder(self, table: str, field: str) -> list[tuple[str | int, str | int, ]]: ...

    @overload
    def fetchInOrder(self, table: str, field: dict[str, str]) -> list[tuple[str | int, str | int, ]]: ...

    def fetchInOrder(self, table: str, field: str | list[str] | dict[str, str]) -> list[tuple[str | int, str | int, ]]:
        """
        Function for fetching database entries in given order.

        Args:
            - table (str): Table name.
            - field (str | list[str] | dict[str, str]):
                    where order = [ASC, DESC])
                    - str: "<field_name> <order>"
                    - list[str]: ["<field_name> <order>", "<field_name> <order>", . . . ]
                    - dict[str, str]: {"<field_name>" : "<order>", . . .}

        Returns: list of records sorted in given order.
        """
        return super().fetchInOrder(table=table, field=field)

    @overload
    def getFieldNames(self, table: str, returnType: str = "list") -> list[str]: ...

    @overload
    def getFieldNames(self, table: str, returnType: str = "int") -> int: ...

    def getFieldNames(self, table: str, returnType: str = "list") -> int | list[str]:
        """
        Function for getting field names.

        Args:
            - table (str) : Table name
            - returnType (str) : requests return type of the function -> list | int.

        Returns:
            - If returnType is "list", then returns list of field names.
            - If returnType is "int", then returns number of fields present.
        """
        return super().getFieldNames(table, returnType)

    def getTable(self, table: str) -> Table:
        """
        Creates Table instance.

        Args:
            table (str) : table name.

        Returns: Table
        """
        if table in self.tables:
            t = Table(table=table, filepath=self.__filepath)
            return t
        else:
            raise(NoSuchTableError(table=table))

    def length(self) -> int:
        """
        Checks if database is empty.

        Returns True if empty, else returns number of tables present.
        """
        return super().length()

    def removeEntry(self, table: str, id: int = -1, keyword: str = "", deleteAllOccurences: bool = False, deleteAll: bool = False) -> bool:
        """
        Function for removing records from database.

        Args:
            - table (str) : Table name
            - id (int) : record id to be deleted.
            - keyword (str) : searches keyword and deletes it.
            - deleteAllOccurences (bool) : When True, deletes all occurences of that keyword.
            - deleteAll (bool) : removes all entries from the specified table.

        Returns:
            True if deleted a record. False if record not found.
        """
        return super().removeEntry(table, id, keyword, deleteAllOccurences, deleteAll)

    @overload
    def searchEntry(self, table: str, id: int = -1, keyword: str = "", returnType: str = "ids", findAllOccurence: bool = False) -> int: ...

    @overload
    def searchEntry(self, table: str, id: int = -1, keyword: str = "", returnType: str = "list", findAllOccurence: bool = True) -> list[tuple[int | str]]: ...

    def searchEntry(self, table: str, id: int = -1, keyword: str = "", returnType: str = "ids", findAllOccurence: bool = False) -> int | list[tuple[int | str]]:
        """
        Function for searching in database.

        Args:
            - table (str) : Table name
            - id (int) : entry id in database
            - keyword (str) : keyword to be searched in database
            - returnType (str) :
                - "list" returns all the records of searched parameter.
                - "ids" returns all the ids of records in which searched parameter is present.
            - findAllOccurences (bool) : when True, returns all the occurences of given keyword.

        Returns: list or int.
        """
        return super().searchEntry(table, id, keyword, returnType, findAllOccurence)

    @overload
    def tableNames(self, count: bool = True, list: bool = False, dictionary: bool = False) -> int: ...

    @overload
    def tableNames(self, count: bool = False, list: bool = True, dictionary: bool = False) -> list[str]: ...

    @overload
    def tableNames(self, count: bool = False, list: bool = False, dictionary: bool = True) -> dict[str, str]: ...

    def tableNames(self, count: bool = False, list: bool = True, dictionary: bool = False) -> int | list[str] | dict[str, str]:
        """
        Accesses tables in a database.

        Args:
            - count (bool) : When True, function returns total number of tables.
            - list (bool) : When True, function returns table names.
            - dictionary (bool) : When True, function returns table names in dict format.
        """
        return super().tableNames(count, list, dictionary)

    @overload
    def updateEntry(self, table: str, values: dict[str, str | int], whereField: str, Is: int) -> bool: ...

    @overload
    def updateEntry(self, table: str, values: dict[str, str | int], whereField: str, Is: str) -> bool: ...

    def updateEntry(self, table: str, values: dict[str, str | int], whereField: str, Is: str | int) -> bool:
        """
        Function for updating values in database.

        Args:
            table (str) : tablename.
            values (dict): key is field name and value is value to be updated.
            field (str) : field name to be checked for entry to be updated.
            whereFieldIs (str | int) : field value to be checked.
        Returns:
            id of the entry inserted.
        """
        return super().updateEntry(table, values, whereField, Is)


def openDatabase(filename: str) -> Database:
    """
    Creates a database and returns a Database object.
    """
    try:
        d = Database(filepath=filename)
        return d
    except FileNotFoundError:
        raise(FileNotFoundError(filename))
