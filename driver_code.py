from src.pydbops.pydbms import *

if __name__ == "__main__":

    # Creating Database instance.
    d = openDatabase(system=Databases.SQLITE, filename="MyDB.db")

    # Creating fields for table
    fields = {"id" : "int(4) primary key", "Name" : "TEXT", "Character" : "TEXT"}

    # Creating table
    d.createTable(tableName="Table1", fields=fields)

    name_dict = {"Eddie" : "Joseph", "Steve" : "Joe", "Robin" : "Maya", "Dustin" : "Gaten", "Lucas" : "Caleb", "Mike" : "Finn", "Will" : "Noah", "Jane" : "Millie", "Nancy" : "Natalia"}
    i = 1
    for char, name in name_dict.items():
        # Adding entry in table with Database instance.
        d.addEntry(table="Table1", values={"id" : i, "Name" : f"{name}", "Character" : f"{char}"})
        i += 1

    # Defining Stored Procedures
    proc = d.createProcedure(name="SELECT_PROC", procedure=["SELECT * FROM Table1", "SELECT Name FROM Table1"])
    # And imidiately calling it.
    print(proc.call())

    # Calling Previously Stored Procedure.
    print(d.callProcedure("SELECT_PROC"))
    
    # Creating Stored Procedure with parameters. Use '$^$' sign to specify position of parameter.
    proc = d.createProcedure(name="SELECT_PROC2", procedure=["SELECT $^$ FROM $^$", "SELECT count($^$) FROM $^$"])
    print(d.callProcedure("SELECT_PROC2", param=["*", "Table1", "Name", "Table1"]))

    # Create 2nd table
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
    
    # Printing sqlite3 version
    print(d.databaseVersion())

    # Printing table names present in database.
    print(d.tableNames())

    # Printing length of the table.
    print(d.length())

    # Removing entry (or entries) with a keyword.
    d.removeEntry(table="Table2", keyword="Shrirang", deleteAllOccurences=True)