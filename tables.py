from pydbops import pydbops
import sqlite3
class Table(pydbops):
    """
    Class for representing tables in database.
    """
    def __init__(self, table:str, filepath:str) -> None:
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
    def addEntry(self, values: dict) -> int:
        """
        Function for inserting values in table.

        Args:
            values (dict): key is field name and value is value to be inserted.

        Returns:
            id of the entry inserted.
        """
        return super().addEntry(self.tableName, values)
    def databaseVersion(self):
        return super().databaseVersion()
    def getFieldNames(self, returnType: str = "list") -> list | int:
        return super().getFieldNames(self.tableName, returnType)
    def length(self) -> int:
        """
        Returns length of table. Returns 0 if table is empty.
        """
        count = self.values(count = True)
        return count
    def searchEntry(self, id: int = -1, keyword: str = "", returnType: str = "ids", findAllOccurence: bool = False) -> list:
        return super().searchEntry(self.tableName, id, keyword, returnType, findAllOccurence)
    def removeEntry(self, id: int = -1, keyword: str = "", deleteAllOccurences: bool = False, deleteAll: bool = False) -> bool:
        return super().removeEntry(self.tableName, id, keyword, deleteAllOccurences, deleteAll)
    def updateEntry(self, values: dict, field: str, whereFieldIs: str | int) -> bool:
        return super().updateEntry(self.tableName, values, field, whereFieldIs)
    def values(self, count:bool = False, list:bool = True) -> int | list:
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