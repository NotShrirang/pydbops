import Database as Database

if __name__ == "__main__":

    # Creating Database instance.
    d = Database.openDatabase("MyDB.db")

    # Creating fields for table
    fields = {"Name" : "TEXT", "Number" : "INTEGER"}

    # Creating table
    d.createTable(tableName="Table1", fields=fields)

    # Creating Table instance
    t1 = d.getTable(table="table1")

    # Adding entry in table with Table instance.
    t1.addEntry(values={"Name": "Shrirang", "Number" : 9404797231})

    # Adding entry in table with Database instance.
    d.addEntry(table="Table1", values={"Name": "Shrirang", "Number" : 9404797231})

    # Searching entry with keyword.
    d.searchEntry(table="Table1", keyword="Shrirang", returnType="ids", findAllOccurence=True)

    # Updating an entry.
    d.updateEntry(table="table1", values={"Number" : 123}, field="Name", whereFieldIs="Shrirang")

    # Removing entry (or entries) with a keyword.
    d.removeEntry("table1", keyword="Shrirang" ,deleteAllOccurences=True)

    # Printing values of whole database.
    print(d)

    # Printing values of a table.
    print(t1)
    
    # Printing sqlite3 version
    print(d.databaseVersion())

    # Printing table names present in database.
    print(d.tableNames())

    # Printing length of the table.
    print(d.length())