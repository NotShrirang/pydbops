import pytest
from pytest import *
from src.pydbops.database import *
from src.pydbops.UserDefinedExceptions import InvalidParameterTypeError, InvalidReturnTypeError, NoSuchTableError

def test_openDatabse():
    with pytest.raises(FileNotFoundError):
        assert openDatabase("mydb.txt") == FileNotFoundError 

def test_Database_ops(db_conn: Database):
    d = db_conn
    assert type(d) is Database, f"Type of d is {type(d)}"
    assert d.createTable("Table1", {"Name" : "TEXT", "Character" : "TEXT"}) is True
    assert d.databaseVersion() =="2.6.0"
    name_dict = {"Eddie" : "Joseph" ,"Steve" : "Joe", "Robin" : "Maya", "Dustin" : "Gaten", "Lucas" : "Caleb", "Mike" : "Finn", "Will" : "Noah", "Jane" : "Millie", "Nancy" : "Natalia"}
    i = 0
    for char, name in name_dict.items():
        i += 1
        m = d.addEntry(table="Table1", values={"Name" : f"{name}", "Character" : f"{char}"})
        assert m == i
    assert d.searchEntry(table="Table1", keyword="Steve", returnType="ids", findAllOccurence=False) == 2
    assert d.length() == 1
    assert d.updateEntry(table="Table1", values={"Character" : "Eleven"}, whereField="Name", Is="Millie") is True
    assert d.addEntry(table="Table1", values={"Name": "Jamie", "Character" : "Vecna"}) == i+1
    assert d.removeEntry(table="Table1", keyword="Vecna", deleteAllOccurences=False) is True
    assert d.tableNames() == ["Table1"]
    assert d.tableNames(count=True) == 1
    assert d.data["Table1"]["Name"] == ['Joseph', 'Joe', 'Maya', 'Gaten', 'Caleb', 'Finn', 'Noah', 'Millie', 'Natalia']
    assert d.data["Table1"]["Character"] == ["Eddie", "Steve", "Robin", "Dustin", "Lucas", "Mike", "Will", "Eleven", "Nancy"]
    assert d.getFieldNames(table="Table1", returnType="list") == ["Name", "Character"]
    assert d.getFieldNames(table="Table1", returnType="int") == 0
    assert d.fetchInOrder(table="Table1", field="Name") == [('Caleb', 'Lucas'), ('Finn', 'Mike'), ('Gaten', 'Dustin'), ('Joe', 'Steve'), ('Joseph', 'Eddie'), ('Maya', 'Robin'), ('Millie', 'Eleven'), ('Natalia', 'Nancy'), ('Noah', 'Will')]
    assert d.fetchInOrder(table="Table1", field=["Name ASC", "Character ASC"]) == [('Caleb', 'Lucas'), ('Finn', 'Mike'), ('Gaten', 'Dustin'), ('Joe', 'Steve'), ('Joseph', 'Eddie'), ('Maya', 'Robin'), ('Millie', 'Eleven'), ('Natalia', 'Nancy'), ('Noah', 'Will')]
    assert d.fetchInOrder(table="Table1", field={"Name" : "DESC", "Character" : "ASC"}) == [('Noah', 'Will'), ('Natalia', 'Nancy'), ('Millie', 'Eleven'), ('Maya', 'Robin'), ('Joseph', 'Eddie'), ('Joe', 'Steve'), ('Gaten', 'Dustin'), ('Finn', 'Mike'), ('Caleb', 'Lucas')]
    assert d.createView(table="Table1", view_name="char_view", columns=['id', 'Character']) == {'id': [1, 2, 3, 4, 5, 6, 7, 8, 9], 'Character': ['Eddie', 'Steve', 'Robin', 'Dustin', 'Lucas', 'Mike', 'Will', 'Jane', 'Nancy']}
    assert d.addEntry(table="Table1", values={"Name": "Jamie", "Character" : "Vecna"}) == i+1
    assert d.createTable("Table2", {"Name" : "TEXT", "Character" : "TEXT"}) is True
    name_dict = {"Eddie" : 1, "Steve" : 2, "Robin" : 3, "Dustin" : 4, "Lucas" : 5, "Mike" : 6, "Will" : 7, "Jane" : 8, "Nancy" : 9}
    for name, num in name_dict.items():
        d.addEntry(table="Table2", values={"Name" : f"{name}", "Character" : f"{num}"})
    assert d.union(tableName1="Table1", tableName2="Table2", column_name="Name") == ['Caleb', 'Dustin', 'Eddie', 'Finn', 'Gaten', 'Jamie', 'Jane', 'Joe', 'Joseph', 'Lucas', 'Maya', 'Mike', 'Millie', 'Nancy', 'Natalia', 'Noah', 'Robin', 'Steve', 'Will']
    assert d.intersection(tableName1="Table1", tableName2="Table2", column_name="Name") == []
    assert d.minus(tableName1="Table1", tableName2="Table2", column_name="Name") == ['Caleb', 'Finn', 'Gaten', 'Jamie', 'Joe', 'Joseph', 'Maya', 'Millie', 'Natalia', 'Noah']
    assert d.createIndex(indexName="MyIndex", tableName="Table1", columnName="Name", unique=False) is True
    assert d.removeEntry(table="Table1", keyword="Vecna", deleteAllOccurences=True)
    assert d.searchEntry(table="Table1", keyword="Steve", returnType="ids", findAllOccurence=False) == 2
    assert d.searchEntry(table="Table1", keyword="Steve", returnType="ids", findAllOccurence=True) == [2]
    assert d.removeEntry(table="Table1", deleteAll=True)
    d.addEntry(table="Table1", values={"Name": "Jamie", "Character" : "Vecna"})
    records = d.dropTable("Table1", getData=True)
    assert records == [("Jamie", "Vecna"), ]
    assert d.dropTable("Table2", getData=False) == []

def test_table_ops(db_conn: Database):
    db_conn.createTable("Table2", {"Name" : "TEXT", "Character" : "TEXT"})
    t2 = db_conn.getTable("Table2")
    assert type(t2) is Table, f"Type of t2 is {type(t2)}"
    value_dict = {"Name" : "Andy", "Character" : "Jake"}
    assert t2.addEntry(values=value_dict) == 1
    assert type(t2.databaseVersion()) is str
    assert t2.getFieldNames(returnType="list") == ["Name", "Character"]
    assert t2.length() == 1
    assert t2.databaseVersion() == "2.6.0"
    assert t2.fetchInOrder(field="Name") == [("Andy", "Jake"),]
    assert t2.fetchInOrder(field=["Name ASC", "Character ASC"]) == [("Andy", "Jake"),]
    assert t2.fetchInOrder(field=["Name ASC", "Character ASC"]) == [("Andy", "Jake"),]
    assert t2.searchEntry(keyword="Jake", returnType="ids") == 1
    assert t2.searchEntry(keyword="Jake", returnType="values") == ('Andy', 'Jake')
    assert t2.updateEntry({"Name" : "Melissa", "Character" : "Amy"}, whereField="oid", Is=1) is True
    assert t2.removeEntry(id=1) is True
    assert t2.removeEntry(keyword="Jake", deleteAllOccurences=True) is True

def test_errors(db_conn: Database):
    d = db_conn
    t2 = d.getTable("Table2")
    with pytest.raises(NoSuchTableError):
        assert d.getTable("table1") == NoSuchTableError
    d.createTable("table1", fields={"Name" : "TEXT", "Character" : "TEXT"})
    d.createTable("table2", fields={"Name" : "TEXT", "Character" : "TEXT"})
    t1 = d.getTable("table2")
    with pytest.raises(InvalidReturnTypeError):
        assert d.getFieldNames(table="table1", returnType="in") == InvalidReturnTypeError
        assert t2.searchEntry(keyword="Jake", returnType="list") == InvalidReturnTypeError
        assert d.tableNames(count=True, dictionary=True) == InvalidReturnTypeError
    with pytest.raises(InvalidParameterTypeError):
        assert t1.fetchInOrder(field=1) == InvalidParameterTypeError
    with pytest.raises(KeyError):
        assert d.data["table3"] == KeyError
        assert d.data["table1"]["mark"] == KeyError
