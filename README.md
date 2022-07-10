<img src="https://github.com/NotShrirang/pydbops/blob/main/src/pydbops/database_image.png" height="200" width="200">

# pydbops
[![PyPI Latest Release](https://img.shields.io/pypi/v/pydbops.svg)](https://pypi.org/project/pydbops/)
![Tests](https://github.com/NotShrirang/pydbops/actions/workflows/test.yml/badge.svg)
[![License](https://img.shields.io/pypi/l/pydbops.svg)](https://github.com/NotShrirang/pydbops/blob/main/LICENSE)

Library for simplifying database operations.
<br>

## Installing pydbops with PyPI :

```sh
pip install pydbops
```

## Importing pydbops:

```sh
import pydbops import *
```
or
```sh
import pydbops as db
```
(You will need to call openDatabase() method using db.)

## Methods in Database:
1. <code>openDatabase()</code> - Creates a database and returns a Database object.
2. <code>createTable()</code> - Creates table of given name.
3. <code>addEntry()</code> - Function for inserting values in database.
4. <code>databaseVersion()</code> - Returns sqlite3 version.
5. <code>getFieldNames()</code> - Function for getting field names.
6. <code>getTable()</code> - Creates Table instance.
7. <code>length()</code> - Returns length of database.
7. <code>removeEntry()</code> - Function for removing records from database.
8. <code>searchEntry()</code> - Function for searching in database.
9. <code>tableNames()</code> - Function for retrieving tables in a database.
10. <code>updateEntry()</code> - Function for updating values in database.

For printing data in database, you can use default print() method by passing Database object in it.

Programming Language : Python 3
<br>
License : MIT License
<br>
Operating System : OS Independent
