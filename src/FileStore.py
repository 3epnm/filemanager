# FileStore.py

import io
import os
import re
import imp
import uuid
import mimetypes
import json
import falcon

from metadata.default import default

class FileStore(object):
    def __init__(self, storage_path, database, uuidgen=uuid.uuid4, fopen=io.open):
        self._storage_path = storage_path
        self._db = database
        self._uuidgen = uuidgen
        self._open = fopen

    def file_path(self, name):
        return os.path.join(self._storage_path, name)


    def read_json(self, uuid):
        path = self.file_path('{uuid}.json'.format(uuid=uuid))

        with open(path) as f:
            data = json.load(f)
        
        return data

    def write_json(self, data):
        uuid = data['uuid']
        name = '{uuid}.json'.format(uuid=uuid)
        path = self.file_path(name)

        with self._open(path, 'w') as outfile:
            json.dump(data, outfile, indent=2, ensure_ascii=True)

        return path

    def read_file(self, name):
        path = self.file_path(name)
        stream = self._open(path, 'rb')
        content_length = os.path.getsize(path)

        return stream, content_length

    def write_file(self, name, data):
        path = self.file_path(name)

        with self._open(path, 'wb') as outfile:
            outfile.write(data.file.read())

        return path

    def get_ext(self, type, name):
        ext = mimetypes.guess_extension(type)

        if ext is None:
            s = name.split('.', 1)
            if len(s) > 1:
                ext = '.' + s[1]

        return ext

    def get_metadata_by_type(self, file, file_path, data):
        module_path = os.path.join(os.path.dirname(__file__), 'metadata')
        module_name = file.type.split('/',1)[0]

        fp, path, desc = imp.find_module(module_name, [ module_path ])
        package = imp.load_module(module_name, fp, path, desc)

        getattr(package, module_name)(file_path, data)

    def get_metadata_by_ext(self, ext, file_path, data):
        module_path = os.path.join(os.path.dirname(__file__), 'metadata')
        module_name = ext

        fp, path, desc = imp.find_module(module_name, [ module_path ])
        package = imp.load_module(module_name, fp, path, desc)

        getattr(package, module_name)(file_path, data)

    def save(self, file, userid):
        ext = self.get_ext(file.type, file.filename)

        uuid = self._uuidgen()

        file_name = '{uuid}{ext}'.format(uuid=uuid, ext=ext)
        file_path = self.write_file(file_name, file)

        data = {}
        data['uuid'] = str(uuid)
        data['name'] = file.filename
        data['type'] = file.type

        data['links'] = []

        data['links'].append({
            'type': 'file',
            'uuid': str(uuid),
            'ext': ext[1:],
            '$ref': '/api/file/{uuid}{ext}'.format(uuid=uuid, ext=ext)
        })

        data['links'].append({
            'type': 'metadata',
            'uuid': str(uuid),
            'ext': 'json',
            '$ref': '/api/file/{uuid}.json'.format(uuid=uuid)
        })

        data['metadata'] = {}

        try:
            self.get_metadata_by_type(file, file_path, data)
            default(file_path, data)
        except ImportError: 
            try:
                self.get_metadata_by_ext(ext[1:], file_path, data)
                default(file_path, data)
            except ImportError: 
                default(file_path, data)

        self.write_json(data)

        if self._db:
            self._db.save(data, userid)

        return data

    def remove(self, uuid):
        data = self.read_json(uuid)
        links = data['links']

        doc = { 
            'message': 'Removed',
            'uuid': uuid,
            'files': []
        }

        for item in links:
            file_name = '{uuid}.{ext}'.format(uuid=item['uuid'], ext=item['ext'])
            file_path = self.file_path(file_name)
            print(file_path)
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                    doc['files'].append({
                        'file': file_name,
                        'message': 'removed'
                    })
                except Exception as inst:
                    doc['files'].append({
                        'file': file_name,
                        'message': str(type(inst))
                    })
            else:
                doc['files'].append({
                    'file': file_name,
                    'message': 'not found'
                })

        return doc