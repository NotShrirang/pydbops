from src.pydbops.pydbops import Pydbops
import sqlite3
from typing import overload


class Table(Pydbops):
    """
    Class for representing tables in database.
    Represents single table in a database.

    Note:
    We recommend you not to create object of this class directly.
    Use getTable(tableName: str) method in Database class to get the specific table.

    Args:
    -----
        - table (str) : name of table
        - filepath (str) : path to the database

    Methods:
    -------
        - addEntry() - Function for inserting values in table.
        - databaseVersion() - Returns sqlite3 version.
        - dropTable() - Function for deleting table.
        - fetchInOrder() - Function for fetching table entries in given order.
        - getFieldNames() - Function for getting field names.
        - length() - Returns length of table. Returns 0 if table is empty.
        - removeEntry() - Function for removing records from table.
        - searchEntry() - Function for searching in table.
        - updateEntry() - Function for updating values in table.
        - values() - Accesses records in a table.
    """
    @property
    def data(self) -> dict[str, list[tuple]]:
        """
        Property data of table. Returns data of table.
        """
        return Table.getData(self=self)

    @property
    def shape(self) -> tuple[int]:
        """
        Property shape of table. Returns shape of table.
        """
        conn = sqlite3.connect(self.__filepath)
        c = conn.cursor()
        rows = c.execute(f"SELECT count(*) FROM {self.tableName}").fetchall()[0][0]
        columns = c.execute(f"PRAGMA table_info('{self.tableName}')").fetchall()
        return (rows, len(columns))

    @property
    def columns(self) -> tuple[str]:
        conn = sqlite3.connect(self.__filepath)
        c = conn.cursor()
        records: list[tuple[str]] = c.execute(f"PRAGMA table_info('{self.tableName}')").fetchall()
        column_list = []
        for record in records:
            column_list.append(record[1])
        return tuple(column_list)

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
        string = string + "_______________________________________________\n"
        return string

    def addColumn(self, columnName: str, columnType: str) -> bool:
        """
        Function for adding columns in table.

        Args:
            - columnName (str): name of column to be added.
            - columnType (str): datatype of the column.

        Returns:
            True if executed.
        """
        return super().addColumn(self.tableName, columnName, columnType)

    def addEntry(self, values: dict[str, str]) -> int:
        """
        Function for inserting values in table.

        Args:
            - values (dict): key is field name and value is value to be inserted.

        Returns:
            id of the entry inserted.
        """
        return super().addEntry(self.tableName, values)
    
    def changeColumn(self, columnName: str, columnType: str) -> bool:
        """
        Function for changing datatypes of columns in table.

        Args:
            - columnName (str): name of column to be changed.
            - columnType (str): new datatype of the column.

        Returns:
            True if executed.
        """
        return super().changeColumn(self.tableName, columnName, columnType)

    def createView(self, view_name: str, columns: list[str], where: str = "", Is: str = "") -> dict[str, list[str]]:
        """
        Function for creating views in table.

        Args:
            - view_name (str): name of view.
            - columns (list): specify the names of the columns to be included in the view.
            - where (str): WHERE clause in standard SQL.
            - Is (str): value to be equated with "where" parameter.
            
            (where and Is parameter and inter-dependent.)

        Returns:
            dictionary representing created view.
        """
        return super().createView(self.tableName, view_name, columns, where, Is)

    def databaseVersion(self) -> str:
        """
        Returns sqlite3 version.
        """
        return super().databaseVersion()

    def dropColumn(self, columnName: str) -> bool:
        """
        Function for dropping columns in table.

        Args:
            - columnName (str): name of column to be dropped.

        Returns:
            True if executed.
        """
        return super().dropColumn(self.tableName, columnName)

    def dropTable(self, getData: bool = True) -> list[tuple[str | int, str | int, ]]:
        """
        Function for deleting table.

        Args:
            - getData (bool): If True, returns all the data before deleting the table.

        Returns: list of records.
        """
        records = super().dropTable(table=self.tableName, getData=getData)
        del self
        return records

    @overload
    def fetchInOrder(self, field: list[str]) -> list[tuple[str | int, str | int, ]]: ...

    @overload
    def fetchInOrder(self, field: str) -> list[tuple[str | int, str | int, ]]: ...

    @overload
    def fetchInOrder(self, field: dict[str, str]) -> list[tuple[str | int, str | int, ]]: ...

    def fetchInOrder(self, field: str | list[str] | dict[str, str]) -> list[tuple[str | int, str | int, ]]:
        """
        Function for fetching table entries in given order.

        Args:
            - field (str | list[str] | dict[str, str]):
                    where order = [ASC, DESC])
                    - str: "<field_name> <order>"
                    - list[str]: ["<field_name> <order>", "<field_name> <order>", . . . ]
                    - dict[str, str]: {"<field_name>" : "<order>", . . .}

        Returns: list of records sorted in given order.
        """
        return super().fetchInOrder(table=self.tableName, field=field)
    
    def getData(self, limit: int = -1, columns: list[str] = []) -> dict[str, list[tuple]]:
        if (limit == -1 and columns == []):
            conn = sqlite3.connect(self.__filepath)
            c = conn.cursor()
            mydata: dict[str, list[tuple]] = {}
            column_names: list[str] = Table.getFieldNames(self, returnType="list")
            for column in column_names:
                c.execute(f"SELECT {column} from {self.tableName}")
                records: list[tuple] = c.fetchall()
                rec_list: list[str] = []
                for record in records:
                    rec_list.append(record[0])
                mydata[column] = rec_list
            c.close()
            return mydata
        elif (limit > -1 and columns == []):
            conn = sqlite3.connect(self.__filepath)
            c = conn.cursor()
            mydata: dict[str, list[tuple]] = {}
            column_names: list[str] = Table.getFieldNames(self, returnType="list")
            for column in column_names:
                c.execute(f"SELECT {column} from {self.tableName} LIMIT '{str(limit)}'")
                records: list[tuple] = c.fetchall()
                rec_list: list[str] = []
                for record in records:
                    rec_list.append(record[0])
                mydata[column] = rec_list
            c.close()
            return mydata
        elif (limit == -1 and columns != []):
            conn = sqlite3.connect(self.__filepath)
            c = conn.cursor()
            mydata: dict[str, list[tuple]] = {}
            for column in columns:
                c.execute(f"SELECT {column} from {self.tableName}")
                records: list[tuple] = c.fetchall()
                rec_list: list[str] = []
                for record in records:
                    rec_list.append(record[0])
                mydata[column] = rec_list
            c.close()
            return mydata
        elif (limit > -1 and columns != []):
            conn = sqlite3.connect(self.__filepath)
            c = conn.cursor()
            mydata: dict[str, list[tuple]] = {}
            for column in columns:
                c.execute(f"SELECT {column} from {self.tableName} LIMIT '{str(limit)}'")
                records: list[tuple] = c.fetchall()
                rec_list: list[str] = []
                for record in records:
                    rec_list.append(record[0])
                mydata[column] = rec_list
            c.close()
            return mydata

    @overload
    def getFieldNames(self, returnType: str = "int") -> int: ...

    @overload
    def getFieldNames(self, returnType: str = "list") -> list[str]: ...

    def getFieldNames(self, returnType: str = "list") -> list[str] | int:
        """
        Function for getting field names.

        Args:
            - returnType (str) : requests return type of the function -> list | int.

        Returns:
            - If returnType is "list", then returns list of field names.
            - If returnType is "int", then returns number of fields present.
        """
        return super().getFieldNames(self.tableName, returnType)

    def join(self, table: str, column: str, type: str = "inner", columns: dict[str, str] = {"*" : ""}) -> list[tuple[str]]:
        """
        Function for joining tables.

        Args:
            - table (str) : second table name.
            - column (str) : the column to be matched.
            - type (str) : the join type. i.e. (INNER, LEFT)
            - columns (dict) : dictionary of form {<table-name> : <column-name>}

        Returns:
            list of records.
        """
        columnNames = "*"
        if columns != {"*" : ""}:
            columnNames = ", ".join(["{}.{}".format(k, v) for k, v in columns.items()])
        conn = sqlite3.connect(self.__filepath)
        c = conn.cursor()
        c.execute(f"""SELECT {columnNames} 
                    FROM {self.tableName} 
                    {type} join {table} ON {self.tableName}.{column} = {table}.{column}""")
        records = c.fetchall()
        c.close()
        return records

    def length(self) -> int:
        """
        Returns length of table. Returns 0 if table is empty.
        """
        count = self.values(count=True)
        return count

    def removeEntry(self, id: int = -1, keyword: str = "", deleteAllOccurences: bool = False, deleteAll: bool = False) -> bool:
        """
        Function for removing records from table.

        Args:
            - id (int) : record id to be deleted.
            - keyword (str) : searches keyword and deletes it.
            - deleteAllOccurences (bool) : When True, deletes all occurences of that keyword.
            - deleteAll (bool) : removes all entries from the specified table.

        Returns:
            True if deleted a record. False if record not found.
        """
        return super().removeEntry(self.tableName, id, keyword, deleteAllOccurences, deleteAll)

    def schema(self) -> dict[str, dict[str, str]]:
        return super().schema(self.tableName)

    @overload
    def searchEntry(self, id: int = -1, keyword: str = "", returnType: str = "ids", findAllOccurence: bool = False) -> int: ...

    @overload
    def searchEntry(self, id: int = -1, keyword: str = "", returnType: str = "list", findAllOccurence: bool = True) -> list[tuple[int | str]]: ...

    def searchEntry(self, id: int = -1, keyword: str = "", returnType: str = "ids", findAllOccurence: bool = False) -> int | list[tuple[int | str]]:
        """
        Function for searching in table.

        Args:
            - id (int) : entry id in database
            - keyword (str) : keyword to be searched in database
            - returnType (str) :
                - "list" returns all the records of searched parameter.
                - "ids" returns all the ids of records in which searched parameter is present.
            - findAllOccurences (bool) : when True, returns all the occurences of given keyword.

        Returns: list or int.
        """
        return super().searchEntry(self.tableName, id, keyword, returnType, findAllOccurence)

    @overload
    def updateEntry(self, values: dict[str, str | int], whereField: str, Is: int) -> bool: ...

    @overload
    def updateEntry(self, values: dict[str, str | int], whereField: str, Is: str) -> bool: ...

    def updateEntry(self, values: dict[str, str | int], whereField: str, Is: str | int) -> bool:
        """
        Function for updating values in table.

        Args:
            - values (dict): key is field name and value is value to be updated.
            - field (str) : field name to be checked for entry to be updated.
            - whereFieldIs (str | int) : field value to be checked.

        Returns: id of the entry updated.
        """
        return super().updateEntry(self.tableName, values, whereField, Is)

    @overload
    def values(self, count: bool = True, list: bool = False) -> int: ...

    @overload
    def values(self, count: bool = False, list: bool = True) -> list[str]: ...

    def values(self, count: bool = False, list: bool = True) -> int | list[str]:
        """
        Accesses records in a table.

        Args:
            - count (bool) : When True, function returns total number of records.
            - list (bool) : When True, function returns records.

        Returns: int or list of records
        """
        conn = sqlite3.connect(self.__filepath)
        c = conn.cursor()
        c.execute(f"SELECT * FROM {self.tableName}")
        records = c.fetchall()
        recordList = []
        for record in records:
            recordList.append(record)
        conn.close()
        if count:
            return len(recordList)
        if list:
            return recordList
        else:
            return recordList
