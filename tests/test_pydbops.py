import pytest
from pydbops.Database import *
from pydbops.UserDefinedExceptions import InvalidReturnTypeError
from pytest import *

def test_Database_ops(db_conn):
    d = db_conn
    assert type(d) is Database, f"Type of d is {type(d)}"
    assert d.createTable("table1", {"Name" : "TEXT", "Character" : "TEXT"}) is True
    name_dict = {"Eddie" : "Joseph" ,"Steve" : "Joe", "Robin" : "Maya", "Dustin" : "Gaten", "Lucas" : "Caleb", "Mike" : "Finn", "Will" : "Noah", "Jane" : "Millie", "Nancy" : "Natalia"}
    i = 0
    for char, name in name_dict.items():
        i += 1
        m = d.addEntry(table="Table1", values={"Name" : f"{name}", "Character" : f"{char}"})
        print(m, i)
        assert m == i
    assert d.searchEntry(table="Table1", keyword="Steve", returnType="ids", findAllOccurence=False) == 2
    assert d.length() == 1
    assert d.updateEntry(table="table1", values={"Character" : "Eleven"}, field="Name", whereFieldIs="Millie") is True
    assert d.addEntry(table="Table1", values={"Name": "Jamie", "Character" : "Vecna"}) == i+1
    assert d.removeEntry("table1", keyword="Vecna", deleteAllOccurences=True) is True
    assert d.tableNames() == ["table1"]
    assert d.tableNames(count=True) == 1
    assert d.getFieldNames(table="table1", returnType="list") == ["Name", "Character"]
    assert d.getFieldNames(table="table1", returnType="int") == 2

def test_table_ops(db_conn):
    db_conn.createTable("table2", {"Name" : "TEXT", "Character" : "TEXT"})
    t1 = db_conn.getTable("table2")
    assert type(t1) is Table, f"Type of t1 is {type(t1)}"
    value_dict = {"Name" : "Andy", "Character" : "Jake"}
    assert t1.addEntry(values=value_dict) is 1
    assert type(t1.databaseVersion()) is str
    assert t1.getFieldNames(returnType="list") == ["Name", "Character"]
    assert t1.length() is 1
    assert t1.searchEntry(keyword="Jake", returnType="ids") is 1
    assert t1.searchEntry(keyword="Jake", returnType="values") == ('Andy', 'Jake')
    assert t1.updateEntry({"Name" : "Melissa", "Character" : "Amy"}, field="oid", whereFieldIs=1) is True
    assert t1.removeEntry(id=1) is True

def test_invalid_return_type(db_conn):
    d = db_conn
    t2 = d.getTable("table2")
    with pytest.raises(InvalidReturnTypeError):
        assert d.getFieldNames(table="table1", returnType="in") == InvalidReturnTypeError
        assert t2.searchEntry(keyword="Jake", returnType="list") == InvalidReturnTypeError
    

