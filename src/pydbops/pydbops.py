from pydbops.UserDefinedExceptions import InvalidReturnTypeError, InvalidParameterType
import sqlite3
from typing import overload


class pydbops():
    """
    Base class for database operations.

    Args :
        filepath (str): path for database file.
    """

    def __init__(self, filepath: str) -> None:
        self.__filepath = filepath
        self.__tables = self.tableNames()
        self._table = ""

    def __str__(self) -> str:
        conn = sqlite3.connect(self.__filepath)
        c = conn.cursor()
        string = ""
        for table in self.__tables:
            string = string + (f"\n\n########## {table} ##########\n\n\t")
            c.execute(f"""SELECT * from {table}""")
            records = c.fetchall()
            fields = self.getFieldNames(table=table, returnType="list")
            for field in fields:
                string = string + f"{field} "
            string = string + "\n"
            i = 0
            for record in records:
                i = i + 1
                string = string + f"{i}. "
                for value in record:
                    string = string + f"{value} "
                string = string + "\n"
        conn.close()
        print(string)
        return string

    def addEntry(self, table: str, values: dict[str, str]) -> int:
        """
        Function for inserting values in database.

        Args:
            table (str) : tablename.
            values (dict): key is field name and value is value to be inserted.

        Returns:
            id of the entry inserted.
        """
        columns = "(" + ", ".join([":{}".format(k) for k, _ in values.items()]) + ")"
        conn = sqlite3.connect(self.__filepath)
        c = conn.cursor()
        print(f"INSERT INTO {table} VALUES {columns}", values)
        c.execute(f"INSERT INTO {table} VALUES {columns}", values)
        conn.commit()
        c.execute(f"SELECT oid FROM {table} WHERE oid = (SELECT MAX(oid) FROM {table})")
        id = c.fetchone()
        conn.close()
        self._table = table
        return int(id[0])

    def createTable(self, tableName: str, fields: dict[str, str]) -> bool:
        """
        Creates table of given name.

        Args:
            - tableName (str) : Name of table.
            - fields (dict) : Dictionary of (columns names : data types)
        Returns:
            - True if executed.
        """
        columns = "(" + ", \n".join(["{} {}".format(k, v) for k, v in fields.items()]) + ")"
        conn = sqlite3.connect(self.__filepath)
        c = conn.cursor()
        c.execute(f"""CREATE TABLE IF NOT EXISTS {tableName} \n {columns}""")
        conn.commit()
        conn.close()
        self._table = tableName
        return True

    def databaseVersion(self) -> str:
        """
        Returns sqlite3 version.
        """
        return sqlite3.version

    @overload
    def getFieldNames(self, table: str, returnType: str = "int") -> int: ...

    @overload
    def getFieldNames(self, table: str, returnType: str = "list") -> list[str]: ...

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
        columns = []
        conn = sqlite3.connect(self.__filepath)
        c = conn.cursor()
        data = c.execute(f"SELECT * FROM {table}")
        conn.close()
        self._table = table
        for column in data.description:
            columns.append(column)
        if returnType == "list":
            fields = []
            for column in columns:
                fields.append(column[0])
            return fields
        elif returnType == "int":
            return len(columns)
        else:
            raise(InvalidReturnTypeError(returnType, function="getFieldNames"))

    def length(self) -> int:
        """
        Checks if database is empty.

        Returns True if empty, else returns number of tables present.
        """
        count = self.tableNames(count=True)
        return count

    @overload
    def orderTable(self, table: str, field: list[str]) -> bool: ...

    @overload
    def orderTable(self, table: str, field: str) -> bool: ...

    @overload
    def orderTable(self, table: str, field: dict[str, str]) -> bool: ...

    def orderTable(self, table: str, field: str | list[str] | dict[str, str]) -> bool:
        if type(field) is str:
            conn = sqlite3.connect(self.__filepath)
            c = conn.cursor()
            c.execute(f"SELECT * FROM {table} ORDER BY {field}")
        elif type(field) is list[str]:
            command = ", ".join(["{}".format(v) for v in field])
            conn = sqlite3.connect(self.__filepath)
            c = conn.cursor()
            c.execute(f"SELECT * FROM {table} ORDER BY {command}")
        elif type(field) is dict[str, str]:
            command = ", ".join(["{} {}".format(k, v) for k, v in field])
            conn = sqlite3.connect(self.__filepath)
            c = conn.cursor()
            c.execute(f"SELECT * FROM {table} ORDER BY {command}")
        else:
            raise(InvalidParameterType(field, function="orderTable"))
        conn.commit()
        conn.close()
        return True


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
        if deleteAll:
            conn = sqlite3.connect(self.__filepath)
            c = conn.cursor()
            c.execute(f"DELETE FROM {table}")  # for deleting all records in given
            conn.commit()
            conn.close()
            self._table = table
            return True
        elif ((deleteAll is False) and (id != -1)):  # for deleting 1 record of given id.
            conn = sqlite3.connect(self.__filepath)
            c = conn.cursor()
            c.execute(f"DELETE from {table} WHERE oid = {id}")
            conn.commit()
            c.execute(f"SELECT * from {table}")
            records = c.fetchall()
            c.execute(f"DELETE from {table}")
            conn.commit()
            conn.close()
            for record in records:
                insert_dictionary = {}
                k = 1
                for value in record:
                    insert_dictionary[str(k)] = value
                    k = k + 1
                print(insert_dictionary)
                self.addEntry(table=table, values=insert_dictionary)
            self._table = table
            return True
        elif (keyword != ""):  # for deleting record of given keyword
            conn = sqlite3.connect(self.__filepath)
            c = conn.cursor()
            c.execute(f"SELECT * from {table}")
            records = c.fetchall()
            c.execute(f"DELETE from {table}")
            conn.commit()
            conn.close()
            for record in records:
                insert_dictionary = {}
                k = 1
                for value in record:
                    insert_dictionary[str(k)] = value
                    k = k + 1
                self.addEntry(table=table, values=insert_dictionary)
            keywordFoundEntries = self.searchEntry(table=table, keyword=keyword, returnType="ids", findAllOccurence=True)
            conn = sqlite3.connect(self.__filepath)
            c = conn.cursor()
            if deleteAllOccurences:
                for id in keywordFoundEntries:
                    c.execute(f"DELETE from {table} WHERE oid = {id}")
                    conn.commit()
            else:
                id = keywordFoundEntries[0]
                c.execute(f"DELETE from {table} WHERE oid = {id}")
                conn.commit()
            conn.close()
            self._table = table
            return True
        return False

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
        if returnType not in ["ids", "values"]:
            raise(InvalidReturnTypeError(returnType, function="searchEntry"))
        conn = sqlite3.connect(self.__filepath)
        c = conn.cursor()
        if id != -1:
            c.execute(f"SELECT * from {table} WHERE oid = {id}")
            records = c.fetchone()
            self._table = table
            return records
        elif keyword != "":
            c.execute(f"SELECT * from {table}")
            records = c.fetchall()
            conn.close()
            ids = []
            i = 1
            for record in records:
                if keyword in record:
                    if findAllOccurence:
                        if returnType == "ids":
                            ids.append(i)
                        else:
                            ids.append(record)
                    else:
                        if returnType == "ids":
                            return i
                        else:
                            return record
                else:
                    pass
                i = i + 1
            self._table = table
            return ids
        else:
            return False

    @overload
    def tableNames(self, count: bool = True, list: bool = False, dictionary: bool = False) -> int: ...

    @overload
    def tableNames(self, count: bool = False, list: bool = True, dictionary: bool = False) -> list[str]: ...

    @overload
    def tableNames(self, count: bool = False, list: bool = False, dictionary: bool = True) -> dict[str, str]: ...

    # Non overloaded Function
    def tableNames(

                    self,

                    # count if True, will return number of tables.
                    count: bool = False,

                    # list if True, will return list of table names.
                    list: bool = True,

                    # dictionary if True, will return dictionary of table names.
                    dictionary: bool = False
                ) -> int | list[str] | dict[str, str]:
        """
        Accesses tables in a database.

        Args:
            - count (bool) : When True, function returns total number of tables.
            - list (bool) : When True, function returns table names.
            - dictionary (bool) : When True, function returns table names in dict format.
        """
        if dictionary or count:
            list = False
        if count and dictionary:
            raise(InvalidReturnTypeError("count", "tableNames"))
        conn = sqlite3.connect(self.__filepath)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = c.fetchall()
        tableList = []
        for table in tables:
            tableList.append(table[0])
        conn.close()
        if count:
            return len(tableList)
        if list:
            return tableList
        if dictionary:
            table_dictionary = {}
            for table in tables:
                table_dictionary[table[0]] = table[0]
            return table_dictionary
        else:
            return tableList

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
        command = ", ".join(["\n{} = :{}".format(k, k) for k, _ in values.items()]) + f"\nWHERE {whereField} = :{whereField}"
        values[whereField] = Is
        conn = sqlite3.connect(self.__filepath)
        c = conn.cursor()
        c.execute(f"""UPDATE {table} SET {command}""", values)
        conn.commit()
        conn.close()
        return True
