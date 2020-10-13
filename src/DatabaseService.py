# DatabaseService.py

import cx_Oracle
import json

class DatabaseService(object):
    def __init__(self, connect_string):
        self.connection = cx_Oracle.connect("filer/VeddelRocker77!@rumburak_low")

    def save_af_file(self, data, userid):
        query = """insert into 
            FILER.AF_FILE(UUID, FILENAME, MIME_TYPE, CREATED_BY, PROPERTIES_JSON) values 
            (:UUID, :FILENAME, :MIMETYPE, :CREATEDBY, :PROPERTIESJSON)"""
        
        cursor = self.connection.cursor()

        try:
            cursor.execute(query, UUID=data['id'], FILENAME=data['name'], MIMETYPE=data['type'], CREATEDBY=userid, PROPERTIESJSON=json.dumps(data, indent=2))
            self.connection.commit()

            ROWID = cursor.lastrowid
        except Exception as inst:
            print(type(inst))
            print(inst.args)

        try:
            cursor.execute("select AF_FILE_ID FROM FILER.AF_FILE where rowid = :1", [ ROWID ])
            row = cursor.fetchone()
        except Exception as inst:
            print(type(inst))
            print(inst.args)
