import json
from src.pydbops.database import *
import sqlite3

class Pydbops_cli():
    def __init__(self) -> None:
        self.filename = ""
        self.database: Database = None
        self.command_list: list = ["create", "CREATE", "switch", "SWITCH", "add", "ADD", "update", "UPDATE", "remove", "REMOVE", "SHOW", "show", "--help", "--execute"]
        self.current_command: str = ""
        self.current_table: str = ""
        database = input("> database path : ")
        self.filename = database
        d: Database = openDatabase(database)
        self.database: Database = d

    def check(self, command:str):
        self.current_command = command
        if (command.split(" ")[0] == "create") or (command.split(" ")[0] == "CREATE"):
            if len(command.split(" ")) == 1:
                print("  Please Valid Table Name!")
                return
            table = command.split(" ")[1]
            fields_dictionary = json.loads(input("  fields = "))
            self.database.createTable(tableName=table, fields=fields_dictionary)
            self.current_table = table
            print(f"  Created {table} Successfully!")
        
        elif (command.split(" ")[0] == "switch") or (command.split(" ")[0] == "SWITCH"):
            if len(command.split(" ")) == 1:
                print("  Please Enter Table Name!")
                return            
            table = command.split(" ")[1]
            if table in self.database.tables:
                self.current_table = table
            else:
                print("  Please Valid Table Name!")
                return

        elif (command.split(" ")[0] == "add") or (command.split(" ")[0] == "ADD"):
            if len(command.split(" ")) == 1:
                if self.current_table == "":
                    print("  Please Enter Table Name!")
                    return
                else:
                    print(f"  Adding entry in default table! {self.current_table}")
                    table = self.current_table
            if self.current_table == "":        
                table = command.split(" ")[1]
            try:
                fields_dictionary = json.loads(input("  values = "))
                if len(fields_dictionary) == 0:
                    raise(ValueError)
            except:
                print("  Please Enter Valid Entry!")
                return
            self.database.addEntry(table=table, values=fields_dictionary)
            print("  Added entry Successfully!")

        elif (command.split(" ")[0] == "update") or (command.split(" ")[0] == "UPDATE"):
            if len(command.split(" ")) == 1:
                if self.current_table == "":
                    print("  Please Enter Table Name!")
                    return
                else:
                    table = self.current_table
            if self.current_table == "":        
                table = command.split(" ")[1]
            try:
                fields_dictionary = json.loads(input("  values = "))
                if len(fields_dictionary) == 0:
                    raise(ValueError)
            except:
                print("  Please Enter Valid Entry!")
                return
            try:
                fieldname = input("  field = ")
                if fieldname == "":
                    raise(ValueError)
            except:
                print("  Please Enter Valid Entry!")
                return
            try:
                field_value = input("  value = ")
                if field_value == "":
                    raise(ValueError)
            except:
                print("  Please Enter Valid Entry!")
                return
            self.database.updateEntry(table=table, values=fields_dictionary, whereField=fieldname, Is=field_value)
            print("  Updated entry Successfully!")

        elif (command.split(" ")[0] == "remove") or (command.split(" ")[0] == "REMOVE"):
            if len(command.split(" ")) == 1:
                if self.current_table == "":
                    print("  Please Enter Table Name!")
                    return
                else:
                    table = self.current_table
            if self.current_table == "":        
                table = command.split(" ")[1]
            id = int(input("  ID = "))
            self.database.removeEntry(table=table, id=id)
            print("  Removed entry Successfully!")

        elif (command.split(" ")[0] == "SHOW") or (command.split(" ")[0] == "show"):
            print(self.database)

        elif (command.split(" ")[0] == "--help"):
            print("""\n  ================= pydbops CLI ==================\n\n  'create' - Create new table,\n  'switch' - Set a table as default,\n  'add' - Add entry to a table,\n  'update' - Update entry in a table,\n  'remove' - Remove an entry,\n  'show' - Display All data.\n  '--help' - You just used it!\n  '--execute' - Directly write SQL query.""")
            return

        elif (command.split(" ")[0] == "--execute"):
            print("  EXECUTE mode :")
            while True:
                exec_command = input("\t-> ")
                if exec_command == "close" or exec_command == "CLOSE":
                    break
                conn = sqlite3.connect(self.filename)
                c = conn.cursor()
                c.execute(exec_command)
                if (exec_command.split(" ")[0] == "SELECT") or (exec_command.split(" ")[0] == "select"):
                    records = c.fetchall()
                    print(records)
                conn.commit()
                conn.close()
