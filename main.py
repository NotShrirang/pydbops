from Database import *

if __name__ == "__main__":
    fields = {"Name" : "TEXT", "Number" : "INTEGER"}
    d = openDatabase("MyDB.db")
    d.createTable("Table1", fields=fields)

    # print(d.addEntry("Table1", {"Name": "Shrirang", "Number" : 9404797231}))
    # print(d.addEntry("Table1", {"Name": "Neil", "Number" : 2}))
    # print(d.addEntry("Table1", {"Name": "Aai", "Number" : 9372074604}))
    # print(d.addEntry("Table1", {"Name": "Baba", "Number" : 9371026821}))

    # d.createTable("Table2", fields={"Name" : "TEXT", "Number" : "INTEGER"})
    # print(d.databaseVersion())
    # print(d.tables())
    # print(d.isEmpty())
    # print(d.addEntry("Table1", {"Name": "Neil", "Number" : 5}))
    # print(d.searchEntry(table="Table1", keyword="Neil", returnType="ids", findAllOccurence=True))
    # d.removeEntry("table1", keyword="Neil" ,deleteAllOccurences=True)
    # d.updateEntry(table="table1", values={"Number" : 6969}, parameter="Name", whereParamterIs="Neil")