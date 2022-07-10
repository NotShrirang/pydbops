from pydbops.pydbops import pydbops
import sqlite3
from typing import overload


class Table(pydbops):
    """
    Class for representing tables in database.
    """
    def __init__(self, table: str, filepath: str) -> None:
        super().__init__(filepath=filepath)
        self.tableName = table
        self.__filepath = filepath

    def __str__(self) -> str:
        if self.length() == 0:
            return f"Table '{self.tableName}' is empty."
        conn = sqlite3.connect(self.__filepath)
        c = conn.cursor()
        string = ""
        string = string + (f"\n\n############### {self.tableName} ###############\n\n")
        c.execute(f"""SELECT * from {self.tableName}""")
        records = c.fetchall()
        fields = self.getFieldNames(returnType="list")
        for field in fields:
            string = f"{string}\t{field} "
        string = f"{string}\n"
        i = 0
        for record in records:
            i = i + 1
            string = string + f"{i}.\t"
            for value in record:
                string = string + f"{value} "
            string = string + "\n"
        conn.close()
        string = string + "_________________________________________________________\n"
        return string

    def addEntry(self, values: dict[str, str]) -> int:
        """
        Function for inserting values in table.

        Args:
            values (dict): key is field name and value is value to be inserted.

        Returns:
            id of the entry inserted.
        """
        return super().addEntry(self.tableName, values)

    def databaseVersion(self) -> str:
        return super().databaseVersion()

    @overload
    def getFieldNames(self, returnType: str = "int") -> int: ...

    @overload
    def getFieldNames(self, returnType: str = "list") -> list[str]: ...

    def getFieldNames(self, returnType: str = "list") -> list[str] | int:
        return super().getFieldNames(self.tableName, returnType)

    def length(self) -> int:
        """
        Returns length of table. Returns 0 if table is empty.
        """
        count = self.values(count=True)
        return count

    @overload
    def searchEntry(self, id: int = -1, keyword: str = "", returnType: str = "ids", findAllOccurence: bool = False) -> int: ...

    @overload
    def searchEntry(self, id: int = -1, keyword: str = "", returnType: str = "list", findAllOccurence: bool = True) -> list[tuple[int | str]]: ...

    def searchEntry(self, id: int = -1, keyword: str = "", returnType: str = "ids", findAllOccurence: bool = False) -> int | list[tuple[int | str]]:
        return super().searchEntry(self.tableName, id, keyword, returnType, findAllOccurence)

    def removeEntry(self, id: int = -1, keyword: str = "", deleteAllOccurences: bool = False, deleteAll: bool = False) -> bool:
        return super().removeEntry(self.tableName, id, keyword, deleteAllOccurences, deleteAll)

    @overload
    def updateEntry(self, values: dict[str, str | int], field: str, whereFieldIs: int) -> bool: ...

    @overload
    def updateEntry(self, values: dict[str, str | int], field: str, whereFieldIs: str) -> bool: ...

    def updateEntry(self, values: dict[str, str | int], field: str, whereFieldIs: str | int) -> bool:
        return super().updateEntry(self.tableName, values, field, whereFieldIs)

    @overload
    def values(self, count: bool = True, list: bool = False) -> int: ...

    @overload
    def values(self, count: bool = False, list: bool = True) -> list[str]: ...

    def values(self, count: bool = False, list: bool = True) -> int | list[str]:
        """
        Accesses tables in a database.

        Args:
            - count (bool) : When True, function returns total number of tables.
            - list (bool) : When True, function returns table names.
        """
        conn = sqlite3.connect(self.__filepath)
        c = conn.cursor()
        c.execute(f"SELECT * FROM {self.tableName}")
        records = c.fetchall()
        recordList = []
        for record in records:
            recordList.append(record[0])
        conn.close()
        if count:
            return len(recordList)
        if list:
            return recordList
        else:
            return recordList
