# pydbops - Relational Database Management System for Python Developers

[![v0.1.2](https://img.shields.io/badge/version-v0.1.2-red.svg?style=flat&logo=)](https://github.com/NotShrirang/pydbops)
[![PyPI Latest Release](https://img.shields.io/pypi/v/pydbops.svg)](https://pypi.org/project/pydbops/)
![Tests](https://github.com/NotShrirang/pydbops/actions/workflows/test.yml/badge.svg)
![Python Package](https://github.com/NotShrirang/pydbops/actions/workflows/python-package.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat&logo=license)](https://github.com/NotShrirang/pydbops/blob/main/LICENSE)
[![Language: Python](https://img.shields.io/badge/language-python-blue.svg?style=flat&logo=python)](https://www.python.org/)
[![Framework: sqlite3](https://img.shields.io/badge/interface-sqlite3-blue.svg?style=flat&logo=sqlite3)](https://docs.python.org/3/library/sqlite3.html#:~:text=SQLite%20is%20a%20C%20library,SQLite%20for%20internal%20data%20storage.)

## Overview

**pydbops** is a robust Relational Database Management System (RDBMS) developed on top of SQLite databases. It provides a convenient Command-Line Interface (CLI) alongside a Python library to simplify database operations. This project aims to enhance the database management experience for Python developers, offering features such as support for stored procedures, which standard SQLite3 does not provide.

## Features

- Simplified database operations
- Support for [stored procedures](https://www.google.com/search?q=sqlite3+standard+procedure)
- Command-Line Interface (CLI) for additional convenience

## Installation

Install **pydbops** using PyPI with the following command:
Library for simplifying database operations.<br>
<b>"pydbops"</b> now supports <a href="https://www.google.com/search?q=sqlite3+standard+procedure">stored procedures</a> which standard sqlite3 doesn't provide!
<br>

## Installing pydbops with PyPI :

```sh
pip install pydbops
```

_(Copy and paste the above command to terminal.)_

## Importing pydbops:

```sh
from pydbops import *
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

## Requirements
- Python > 3.5
- SQLite3

## License
This project is licensed under the MIT License. Feel free to explore and contribute to the development of pydbops!
