# DatabaseService.py

import cx_Oracle
import json

class DatabaseService(object):
    def __init__(self, connect_string):
        con = cx_Oracle.connect("filer/VeddelRocker77!@rumburak_low")

        print("Database version:", con.version)
        cur = con.cursor()
        cur.execute("select * from all_objects where rownum <= 10")
        res = cur.fetchall()

        for row in res:
            print(row)

