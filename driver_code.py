from src.pydbops.Database import * 
from src.pydbops.pydbops import *

if __name__ == "__main__":

    # Creating Database instance.
    d = openDatabase("MyDB.db")

    # Creating fields for table
    fields = {"Name" : "TEXT", "Character" : "TEXT"}

    # Creating table
    d.createTable(tableName="Table1", fields=fields)

    name_dict = {"Eddie" : "Joseph", "Steve" : "Joe", "Robin" : "Maya", "Dustin" : "Gaten", "Lucas" : "Caleb", "Mike" : "Finn", "Will" : "Noah", "Jane" : "Millie", "Nancy" : "Natalia"}
    for char, name in name_dict.items():
        # Adding entry in table with Database instance.
        d.addEntry(table="Table1", values={"Name" : f"{name}", "Character" : f"{char}"})

    d.createTable(tableName="Table2", fields={"Name" : "TEXT", "Number" : "INTEGER"})

    # Creating an index
    d.createIndex(indexName="MyIndex", tableName="Table1", columnName="Name", unique=False)

    # Creating Table instance
    t2 = d.getTable(table="Table2")

    # Adding entry in table with Table instance.
    t2.addEntry(values={"Name": "Shrirang", "Number" : 123456789})

    # Adding entry in table with Database instance.
    d.addEntry(table="Table2", values={"Name": "Shrirang", "Number" : 123456789})

    # Searching entry with keyword.
    d.searchEntry(table="Table2", keyword="Shrirang", returnType="ids", findAllOccurence=True)

    # Updating an entry.
    d.updateEntry(table="Table2", values={"Number" : 987654321}, whereField="Name", Is="Shrirang")

    # Printing values of whole database.
    print(d)

    # Printing values of a table.
    print(t2)
    
    # Removing entry (or entries) with a keyword.
    d.removeEntry(table="Table2", keyword="Shrirang", deleteAllOccurences=True)
    
    # Printing sqlite3 version
    print(d.databaseVersion())

    # Printing table names present in database.
    print(d.tableNames())

    # Printing length of the table.
    print(d.length())
