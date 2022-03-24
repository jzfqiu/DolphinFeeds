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
        self.cursor = self.cnx.cursor()


    def insert(self, table, data: List[Dict]):
        while data:
            row = data.pop(0)
            insert = list(row.keys())
            filler = ["%s" for _ in range(len(row))]
            values = []
            for value in row.values():
                if isinstance(value, list):
                    values.append(",".join(value))
                else:
                    values.append(value)
            query = "INSERT INTO {} ({}) VALUES ({});".format(
                table, ', '.join(insert), ", ".join(filler))    
            self.cursor.execute(query, values)
        self.cnx.commit()
        res = self.cursor.fetchall()
        return res


    def filter(self, table: str, data: Dict):
        query = "SELECT * FROM {} WHERE ".format(table)
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
        res = self.cursor.fetchall()
        return res

    def close(self):
        self.cursor.close()
        self.cnx.close()

        


