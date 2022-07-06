import sqlite3
from xml.etree.ElementPath import find
from UserDefinedExceptions import *


class Database:
    """
    Class for database operations.
    Args :
        filepath (str): path for database file.
    """
    def __init__(self, filepath:str) -> None:
        self.__filepath = filepath
        self.__columnNames = []
        self.__tableNames = []
        self.__tableNames = self.tables()

    def addEntry(self, table:str, value:dict) -> int:
        """
        Function for inserting values in database.

        Args:
            table (str) : tablename.
            value (dict): key is column name and value is value to be inserted.

        Returns:
            id of the entry inserted.
        """
        columns = "(" + ", ".join([":{}".format(k) for k,_ in value.items()]) + ")"
        conn = sqlite3.connect(self.__filepath)
        c = conn.cursor()
        c.execute(f"INSERT INTO {table} VALUES {columns}", value)
        conn.commit()
        c.execute(f"SELECT oid FROM {table} WHERE oid = (SELECT MAX(oid) FROM {table})")
        id = c.fetchone()
        conn.close()
        return id[0]

    def createTable(self, tableName:str, fields:dict) -> bool:
        columns = "(" + ",\n".join(["{} {}".format(k,v) for k,v in fields.items()]) + ")"
        conn = sqlite3.connect(self.__filepath)
        c = conn.cursor()
        c.execute(f"""CREATE TABLE IF NOT EXISTS {tableName} \n {columns}""")
        conn.commit()
        conn.close()

    def databaseVersion(self):
        return sqlite3.version

    def isEmpty(self) -> bool | int:
        count = self.tables(count = True)
        if count == 0:
            return True
        else:
            return count

    def removeEntry(self, table:str, id: int = -1, keyword: str = "", deleteAllOccurences: bool = False , deleteAll: bool = False) -> bool:
        if deleteAll:
            conn = sqlite3.connect(self.__filepath)
            c = conn.cursor()
            c.execute(f"DELETE FROM {table}") # for deleting all records in given 
            conn.commit()
            conn.close()
            return True
        elif (deleteAll == False and id != -1) : # for deleting 1 record of given id.
            conn = sqlite3.connect(self.__filepath)
            c = conn.cursor()
            c.execute(f"DELETE from {table} WHERE oid = {id}")
            conn.commit()
            conn.close()
            return True
        elif (keyword != "") : # for deleting record of given keyword
            keywordFoundEntries = self.searchEntry(table=table, keyword=keyword, returnType="ids", findAllOccurence=True)
            conn = sqlite3.connect(self.__filepath)
            c = conn.cursor()
            if deleteAllOccurences:
                for id in keywordFoundEntries:
                    
                    # self.removeEntry(table=table, deleteAll=True)
                    c.execute(f"DELETE from {table} WHERE oid = {id}")
                    conn.commit()
            else:
                id = keywordFoundEntries[0]
                c.execute(f"DELETE from {table} WHERE oid = {id}")
                conn.commit()
            conn.close()

    def searchEntry(self, table:str, id:int = -1, keyword:str = "", returnType:str = "ids", findAllOccurence:bool = False) -> list:
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

        Returns: list.
        """
        
        if returnType in ["ids", "values"]:
            pass
        else:
            raise(InvalidReturnTypeError(returnType))
        conn = sqlite3.connect(self.__filepath)
        c = conn.cursor()
        if id != -1:
            c.execute(f"SELECT * from {table} WHERE oid = {id}")
            records = c.fetchone()
            return records
        elif keyword!="":
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
            return ids
        
    def tables(self, count:bool = False, list:bool = True) -> list|int:
        """
        Accesses tables in a database.
        Args:
            - count (bool) : When True, function returns total number of tables.
            - list (bool) : When True, function returns table names. 
        """
        conn = sqlite3.connect(self.__filepath)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = c.fetchall()
        tableList = []
        for table in tables:
            tableList.append(table[0])
        conn.close()
        if count == True:
            return len(tableList)
        if list == True:
            return tableList
        else:
            return tableList
