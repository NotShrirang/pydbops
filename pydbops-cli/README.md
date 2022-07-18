# pydbops CLI

Simple command line interface for database management.

Check out <a href="https://github.com/NotShrirang/pydbops/releases">Releases</a> for downloads

After installation, include <code>pydbops-cli-x86_64</code> folder to environment variable <code>PATH</code>.

## To start session:

```
pydb connect
```

or

```
pydb init
```

Useful commands:

1. <code>CREATE <_table_name_></code> -
    - Asks for field names names.
    - Provide dictionary with comma-separated values <code>{ "<_field_name1_>" : "<_data_type_>", "<_field_name2_>" : "<_data_type_>", ...  }</code>
    - Creates Table of given name.

2. <code>SWITCH <_table_name_></code> - Sets default table. (You don't need to write table name each time you run query after this.)
3. <code>ADD_table_name_></code> -
    - Asks for dictionary of values.
    - Provide dictionary with comma-separated values <code>{ "<_field_name1_>" : "<_field_value_>", "<_field_name2_>" : "<_field_value_>", ...  }</code>
    - Adds value to given table.
4. <code>UPDATE <_table_name_></code> - Updates entry.
5. <code>REMOVE <_table_name_></code> - Removes entry of given id.
6. <code>SHOW</code> - Displays whole database.
7. <code>--help</code> - Shows helpful commands.
8. <code>--execute</code> - Allows standard SQL queries to be executed.

## Requirements:
- Python >= 3.6 - <a href="https://www.python.org/">python.org</a>
- Windows - x86 (64 bit.)
