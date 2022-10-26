from hashlib import sha256
import sqlite3


class Procedure():
    """
    Procedure class
    """
    def __init__(self, name: str = "", procedure: list[str] = "", connection: str = "", add: bool = False) -> None:
        self.name: str = name
        self.conn: str = connection
        self.outputs: list[list[str]] = []
        self.procedure: list[str] = procedure
        if add:
            self.addProc()

    def addProc(self):
        """
        Function of storing procedures in the database.
        """
        procs = "!^!".join(self.procedure)
        conn = sqlite3.connect(self.conn)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS pydbops_procedures (proc_id varchar(256) primary key, procedure text)")
        conn.commit()
        c.execute(f"""INSERT INTO pydbops_procedures (proc_id, procedure) VALUES 
                    ('{sha256(self.name.encode('utf-8')).hexdigest()}',
                    '{procs}');""")
        conn.commit()
        conn.close()

    def call(self, param: list = []) -> list:
        """
        Function for calling stored procedure.
        
        Args:
            - param: list = list of parameters.
        
        Returns:
            - Data returned by procedure.
        """
        if param == []:
            self.procedure = self.parse(self.name, self.conn, param=param)
            conn = sqlite3.connect(self.conn)
            c = conn.cursor()
            try:
                for proc in self.procedure:
                    c.execute(proc)
                    records = c.fetchall()
                    self.outputs.append(records)
            except sqlite3.OperationalError as e:
                if 'unrecognized token: "$"' in e.args:
                    print("pydbops.OperationalError : Parameters not provided")
                    exit(1)
                else:
                    print(sqlite3.OperationalError, f": {e}")
                    exit(1)
            c.close()
            conn.commit()
            conn.close()
            return self.outputs
        else:
            self.procedure = self.parse(self.name, self.conn, param=param)
            conn = sqlite3.connect(self.conn)
            c = conn.cursor()
            for proc in self.procedure:
                c.execute(proc)
                records = c.fetchall()
                self.outputs.append(records)
            c.close()
            conn.commit()
            conn.close()
            return self.outputs

    def parse(self, name: str, connection: str, param: list) -> list[str]:
        """
        Function for parsing sql queries.
        
        Args:
            - name: str = name of procedure.
            - param: list = list of parameters.
        
        Returns:
            - Data returned by procedure.
        """
        conn = sqlite3.connect(connection)
        c = conn.cursor()
        procedure: str = c.execute(f"SELECT procedure FROM pydbops_procedures WHERE proc_id = '{sha256(name.encode('utf-8')).hexdigest()}'").fetchall()[0][0]
        for p in param:
            procedure = procedure.replace("$^$", p, 1)
        instructions = procedure.split("!^!")
        c.close()
        conn.commit()
        conn.close()
        return instructions