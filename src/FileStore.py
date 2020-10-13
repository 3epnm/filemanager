# FileStore.py

import io
import os
import re
import uuid
import mimetypes
import json
import falcon

from metadata.ImageMetadata import ImageMetadata
from metadata.PdfMetadata import PdfMetadata

class FileStore(object):
    _IMAGE_NAME_PATTERN = re.compile(
        '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.[a-z]{2,4}$'
    )

    def __init__(self, storage_path, database, uuidgen=uuid.uuid4):
        self._storage_path = storage_path
        self._db = database
        self._uuidgen = uuidgen

    def file_path(self, name):
        return os.path.join(self._storage_path, name)

    def read_metadata(self, name):
        uuid = os.path.splitext(name)[0]
        path = self.file_path('{uuid}.json'.format(uuid=uuid))

        with open(path) as f:
            data = json.load(f)
        
        return data

    def open_file(self, name, fopen=io.open):
        # if not self._IMAGE_NAME_PATTERN.match(name):
        #     raise IOError('File not found')

        path = self.file_path(name)
        stream = fopen(path, 'rb')
        content_length = os.path.getsize(path)

        return stream, content_length

    def save_file(self, name, data, fopen=io.open):
        path = self.file_path(name)

        with fopen(path, 'wb') as outfile:
            outfile.write(data.file.read())

        return path

    def save_json(self, uuid, data, fopen=io.open):
        name = '{uuid}.json'.format(uuid=uuid)
        path = self.file_path(name)

        with fopen(path, 'w') as outfile:
            json.dump(data, outfile, indent=2, ensure_ascii=True)

        return path

    def save(self, file, userid):
        ext = mimetypes.guess_extension(file.type)
        uuid = self._uuidgen()

        file_name = '{uuid}{ext}'.format(uuid=uuid, ext=ext)
        file_path = self.save_file(file_name, file)

        data = {}
        data['id'] = str(uuid)
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

        ImageMetadata(file_path, data)
        PdfMetadata(file_path, data)

        self.save_json(uuid, data)

        self._db.save_af_file(data, userid)

        return data