from pydbops.database import Database
from src.pydbops.UserDefinedExceptions import InvalidReturnTypeError, InvalidParameterTypeError
from src.pydbops.procedures import Procedure
import sqlite3
from typing import Any, overload
import platforms_names as platform



class Pydbops():
    """
    Base class for database operations.

    Args :
        filepath (str): path for database file.
    """

    def __init__(self, filepath: str) -> None:
        self.__filepath = filepath
        self.__tables = self.tableNames()
        self._table = ""
        self.triggers: str = []

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
        return string

    def addColumn(self, table: str, columnName: str, columnType: str) -> bool:
        """
        Function for adding columns in database.

        Args:
            table (str) : tablename.
            columnName (str): name of column to be added.
            columnType (str): datatype of the column.

        Returns:
            True if executed.
        """
        conn = sqlite3.connect(self.__filepath)
        c = conn.cursor()
        c.execute(f"""ALTER TABLE {table}
                    ADD {columnName} {columnType}
                    """)
        conn.commit()
        conn.close()
        self._table = table
        return True

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
        c.execute(f"INSERT INTO {table} VALUES {columns}", values)
        conn.commit()
        c.execute(f"SELECT oid FROM {table} WHERE oid = (SELECT MAX(oid) FROM {table})")
        id = c.fetchone()
        conn.close()
        self._table = table
        return int(id[0])

    def callProcedure(self, name: str, param: list = []) -> list:
        """
        Function for calling stored procedure.
        
        Args:
            - name: str = name of the procedure.
            - param: list = list of parameters (optional)
        
        Returns:
            - Data returned by procedure.
        """
        proc = Procedure(name, connection = self.__filepath)
        records = proc.call(param=param)
        return records

    def changeColumn(self, table: str, columnName: str, columnType: str) -> bool:
        """
        Function for changing datatypes of columns in database.

        Args:
            table (str) : tablename.
            columnName (str): name of column to be changed.
            columnType (str): new datatype of the column.

        Returns:
            True if executed.
        """
        conn = sqlite3.connect(self.__filepath)
        c = conn.cursor()
        c.execute(f"""ALTER TABLE {table}
                    MODIFY {columnName} {columnType}
                    """)
        conn.commit()
        conn.close()
        self._table = table
        return True

    def createProcedure(self, name: str, procedure: list[str]) -> Procedure:
        """
        Function for creating and storing procedure.
        
        Args:
            - name: str = name of the procedure.
            - procedure: list[str] = list of sql queries.
        
        Returns:
            - Procedure object.
        """
        new_procedure = Procedure(name, procedure, self.__filepath, add=True)
        return new_procedure

    def createTrigger(self, table: str, on: str, before: bool = True, after: bool = False, ) -> bool | Any:
        """
        Function for creating triggers on tables.

        Args:
            - table: str = name of the table.
            - on: str = CREATE | DELETE | UPDATE
            - before: bool = Trigger to be executed before event? (default = True)
            - after: bool = Trigger to be executed after event? (default = False)
        """
        conn = sqlite3.connect(self.__filepath)
        c = conn.cursor()
        c.execute()


    def createView(self, table: str, view_name: str, columns: list[str] = ["*"], where: str = "", Is:str = "") -> dict[str, list[str]]:
        """
        Function for creating views in database.

        Args:
            - table (str) : tablename.
            - view_name (str): name of view.
            - columns (list): specify the names of the columns to be included in the view.
            - where (str): WHERE clause in standard SQL.
            - Is (str): value to be equated with "where" parameter.
            
            (where and Is parameter and inter-dependent.)

        Returns:
            dictionary representing created view.
        """
        columns_str: str = ", ".join(["{}".format(col) for col in columns])
        conn = sqlite3.connect(self.__filepath)
        c = conn.cursor()
        if (where == "") and (Is == ""):
            c.execute(f"""CREATE VIEW {view_name} AS SELECT {columns_str} FROM {table}""")
        elif (where != "") and (Is != ""):
            c.execute(f"""CREATE VIEW {view_name} AS SELECT {columns_str} FROM {table} WHERE {where} = '{Is}'""")
        else:
            print("Pass both 'where' and 'Is'.")
            exit(1)
        conn.commit()
        view_dict: dict[str, list[str]] = {}
        for column in columns:
            c.execute(f"SELECT {column} from {view_name}")
            records: list[tuple[str]] = c.fetchall()
            rec_list: list[str] = []
            for record in records:
                rec_list.append(record[0])
            view_dict[column] = rec_list
        return view_dict

    def databaseVersion(self) -> str:
        """
        Returns sqlite3 version.
        """
        return sqlite3.version

    def dropColumn(self, table: str, columnName: str) -> bool:
        """
        Function for dropping columns in database.

        Args:
            table (str) : tablename.
            columnName (str): name of column to be dropped.

        Returns:
            True if executed.
        """
        conn = sqlite3.connect(self.__filepath)
        c = conn.cursor()
        c.execute(f"""ALTER TABLE {table}
                    DROP COLUMN {columnName}
                    """)
        conn.commit()
        conn.close()
        self._table = table
        return True

    def dropTable(self, table: str, getData: bool = True) -> list[tuple[str | int, str | int, ]]:
        """
        Function for deleting table.

        Args:
            - table (str): Table name.
            - getData (bool): If True, returns all the data before deleting the table.

        Returns: list of records.
        """
        conn = sqlite3.connect(self.__filepath)
        c = conn.cursor()
        if getData:
            c.execute(f"SELECT * FROM {table}")
            records = c.fetchall()
            c.execute(f"DROP TABLE {table}")
            conn.commit()
            conn.close()
            return records
        else:
            records = []
            c.execute(f"DROP TABLE {table}")
            conn.commit()
            conn.close()
            return []

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
        if type(field) is str:
            conn = sqlite3.connect(self.__filepath)
            c = conn.cursor()
            c.execute(f"SELECT * FROM {table} ORDER BY Name")
        elif type(field) is list:
            command = ", ".join(["{}".format(v) for v in field])
            conn = sqlite3.connect(self.__filepath)
            c = conn.cursor()
            c.execute(f"SELECT * FROM {table} ORDER BY {command}")
        elif type(field) is dict:
            command = ", ".join(["{} {}".format(k, v) for k, v in field.items()])
            conn = sqlite3.connect(self.__filepath)
            c = conn.cursor()
            c.execute(f"SELECT * FROM {table} ORDER BY {command}")
        else:
            raise(InvalidParameterTypeError(field, function="orderTable"))
        records = c.fetchall()
        conn.commit()
        conn.close()
        return records

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
        c.execute(f"SELECT * FROM {table}")
        self._table = table
        if returnType == "list":
            fields = list(map(lambda x: x[0], c.description))
            conn.close()
            return fields
        elif returnType == "int":
            conn.close()
            return len(columns)
        else:
            conn.close()
            raise(InvalidReturnTypeError(returnType, function="getFieldNames"))

    def length(self) -> int:
        """
        Checks if database is empty.

        Returns True if empty, else returns number of tables present.
        """
        count = self.tableNames(count=True)
        return count

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
            conn.close()
            self._table = table
            return True
        elif (keyword != ""):  # for deleting record of given keyword
            keywordFoundEntries = Pydbops.searchEntry(self, table=table, keyword=keyword, returnType="ids", findAllOccurence=True)
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

    def schema(self, table: str) -> dict[str, dict[str, str]]:
        """
        Function for fetching schema of a table in database.

        Args:
            - table (str) : Table name

        Returns: dict.
        """
        conn = sqlite3.connect(self.__filepath)
        c = conn.cursor()
        records: list[tuple[str]] = c.execute(f"PRAGMA table_info('{table}')").fetchall()
        schema: dict[str, dict[str, str]] = {}
        for record in records:
            schema[record[1]] = {'cid' : record[0], 'dtype' : record[2], 'notNull' : record[3], 'defaultValue' : record[4], 'pri' : record[5]}
        return schema

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
        self._table = table
        if returnType not in ["ids", "values"]:
            raise(InvalidReturnTypeError(returnType, function="searchEntry"))
        conn = sqlite3.connect(self.__filepath)
        c = conn.cursor()
        if id != -1:
            c.execute(f"SELECT * from {table} WHERE oid = {id}")
            records = c.fetchone()
            self._table = table
            conn.close()
            return records
        elif keyword != "":
            ids: list[int] = []
            columns = Pydbops.getFieldNames(self, table=table, returnType="list")
            for columnName in columns:
                c.execute(f"SELECT oid from {table} WHERE {columnName} = '{str(keyword)}'")
                recs: list = c.fetchall()
                for id in recs:
                    ids.append(id[0])
            if findAllOccurence:  # All occurences
                if returnType == "ids":
                    conn.close()
                    return ids
                else:
                    c.execute(f"SELECT * from {table} WHERE {columnName} = '{str(keyword)}'")
                    conn.close()
                    recs = c.fetchall()
                    return recs
            else:  # First occurence
                if returnType == "ids":
                    conn.close()
                    return ids[0]
                else:
                    c.execute(f"SELECT * from {table} WHERE {columnName} = '{str(keyword)}'")
                    recs = c.fetchall()
                    conn.close()
                    return recs[0]
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
            id of the entry updated.
        """
        command = ", ".join(["\n{} = :{}".format(k, k) for k, _ in values.items()]) + f"\nWHERE {whereField} = :{whereField}"
        values[whereField] = Is
        conn = sqlite3.connect(self.__filepath)
        c = conn.cursor()
        c.execute(f"""UPDATE {table} SET {command}""", values)
        conn.commit()
        conn.close()
        return True
