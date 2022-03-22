from datetime import datetime
from typing import List, Dict
from mysql import connector
from config import *

class Database:

    def __init__(self):
        self.cnx = connector.connect(
            host=RDS_ENDPOINT,
            user=RDS_USER,
            password=RDS_PWD,
            database=RDS_DATABASE
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
            # TODO: rewrite type conversion to for more flexibility
            # while row:
            #     col, val = row.pop(0)
            #     insert.append(col)
            #     if isinstance(val, str):
            #         values.append("'{}'".format(val))
            #     elif isinstance(val, datetime):
            #         values.append("'{}'".format(val.strftime("%Y-%m-%d %H:%M:%S")))
            #     elif isinstance(val, list):
            #         values.append("'{}'".format(" ".join(val)))
            #     else:
            #         values.append("{}".format(val))
            query = "INSERT INTO {} ({}) VALUES ({});".format(
                table, ', '.join(insert), ", ".join(filler))    
            self.cursor.execute(query, values)
        self.cnx.commit()
        res = self.cursor.fetchall()
        return res


    def filter(self, table, data):
        query = "SELECT * FROM {} WHERE ".format(table)
        criteria = list(data.items())
        while criteria:
            col, val = criteria.pop(0)
            if isinstance(val, str):
                query += "{} = '{}'".format(col, val)
            elif isinstance(val, datetime):
                query += "{} = '{}'".format(col, val.strftime("%Y-%m-%d %H:%M:%S"))
            else:
                query += "{} = {}".format(col, val)
            if criteria:
                query += " AND "
        query += ";"
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        return res

    def close(self):
        self.cursor.close()
        self.cnx.close()

        


