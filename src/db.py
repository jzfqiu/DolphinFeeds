from typing import List, Dict
from mysql import connector
from config import *

class Database:

    def __init__(self, host, user, password, database):
        self.cnx = connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.cnx.cursor(buffered=True)


    def insert_many(self, table, data: List[Dict]):
        while data:
            row = data.pop(0)
            insert = list(row.keys())
            filler = ["%s" for _ in range(len(row))]
            values = []
            for value in row.values():
                if isinstance(value, list):
                    values.append(",".join(value))
                else:
                    values.append(str(value))
            query = "INSERT INTO {} ({}) VALUES ({});".format(
                table, ', '.join(insert), ", ".join(filler))    
            self.cursor.execute(query, values)
        self.cnx.commit()
        return self.cursor.rowcount

    def insert_one(self, table, data: Dict):
        insert = list(data.keys())
        filler = ["%s" for _ in range(len(data))]
        values = []
        for value in data.values():
            if isinstance(value, list):
                values.append(",".join(value))
            else:
                values.append(str(value))
        query = f"INSERT INTO {table} ({', '.join(insert)}) VALUES ({', '.join(filler)});"
        self.cursor.execute(query, values)
        self.cnx.commit()
        return self.cursor.rowcount


    def filter(self, table: str, data: Dict):
        query = f"SELECT * FROM {table} WHERE "
        criteria = list(data.items())
        values = []
        while criteria:
            col, val = criteria.pop(0)
            query += "{} = %s ".format(col)
            values.append(val)
            if criteria:
                query += "AND "
        query += ";"
        self.cursor.execute(query, values)
        if self.cursor.with_rows:
            return self.cursor.fetchall()
        else:
            return []


    def update_by_id(self, table, id, updated_row):
        values = list(updated_row.values()) + [id]
        cols = ', '.join([col+"=%s" for col in updated_row.keys()])
        query = f"UPDATE {table} SET {cols} WHERE id=%s;"
        self.cursor.execute(query, values)
        self.cnx.commit()
        return self.cursor.rowcount


    def close(self):
        self.cursor.close()
        self.cnx.close()

        


