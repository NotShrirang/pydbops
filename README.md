<a href="https://pypi.org/project/pydbops/"><img src="https://github.com/NotShrirang/pydbops/blob/main/src/pydbops/database_image.png" height="100" width="100"></a>

# pydbops

[![v0.0.6](https://img.shields.io/badge/version-v0.0.6-red.svg?style=flat&logo=)](https://github.com/NotShrirang/pydbops)
[![PyPI Latest Release](https://img.shields.io/pypi/v/pydbops.svg)](https://pypi.org/project/pydbops/)
![Tests](https://github.com/NotShrirang/pydbops/actions/workflows/test.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat&logo=license)](https://github.com/NotShrirang/pydbops/blob/main/LICENSE)
[![Language: Python](https://img.shields.io/badge/language-python-blue.svg?style=flat&logo=python)](https://www.python.org/)

Library for simplifying database operations.
<br>

## Installing pydbops with PyPI :

```sh
pip install pydbops
```

_(Copy and paste the above command to terminal.)_

## Importing pydbops:

```sh
import pydbops import *
```

or

```sh
import pydbops as db
```

_(You will need to call openDatabase() method using db.)_

## Using CLI:

- Check <a href="https://github.com/NotShrirang/pydbops/releases/tag/v0.0.1">Releases</a>
- <a href="https://github.com/NotShrirang/pydbops/releases/download/v0.0.1/pydbops-cli-installer-X86_64.exe">Download</a> Installer
- <a href="https://github.com/NotShrirang/pydbops/tree/main/pydbops-cli#pydbops-cli">Read about CLI</a>

## Methods in Database:

1. <code>openDatabase()</code> - Creates a database and returns a Database object.
2. <code>createTable()</code> - Creates table of given name.
3. <code>addColumn()</code> - Function for adding new column.
4. <code>addEntry()</code> - Function for inserting values in database.
5. <code>changeColumn()</code> - Function for chnaging column type.
6. <code>createView()</code> - Creates view of given name.
7. <code>databaseVersion()</code> - Returns sqlite3 version.
8. <code>dropColumn()</code> - Function for deleting column.
9. <code>dropTable()</code> - Function for deleting table.
10. <code>fetchInOrder()</code> - Function for fetching database entries in given order.
11. <code>getData()</code> - Function for getting all data.
12. <code>getFieldNames()</code> - Function for getting field names.
13. <code>getTable()</code> - Creates Table instance.
14. <code>intersection()</code> - Performs intersection and returns all distinct rows selected by query.
15. <code>join()</code> - Performs SQL Join on table specified.
15. <code>length()</code> - Returns length of database.
16. <code>minus()</code> - Fetches rows which are present in first query but absent in second.
17. <code>removeEntry()</code> - Function for removing records from database.
18. <code>schema()</code> - Function for fetching schema of table in database.
19. <code>searchEntry()</code> - Function for searching in database.
20. <code>tableNames()</code> - Function for retrieving tables in a database.
21. <code>union()</code> - Performs union and returns all distinct rows selected by query.
22. <code>updateEntry()</code> - Function for updating values in database.

For printing data in database, you can use default print() method by passing Database object in it.

## Requirements:
- Python > 3.5
- sqlite3