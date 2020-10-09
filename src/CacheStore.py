# CacheStore.py

import io
import os
import re
import uuid
import mimetypes
import json
import falcon

class CacheStore(object):
    def __init__(self, cache_path, uuidgen=uuid.uuid4):
        self._cache_path = cache_path
        self._uuidgen = uuidgen

    def file_path(self, name):
        return os.path.join(self._cache_path, name)

    def open_file(self, name, fopen=io.open):
        image_path = self.file_path(name)
        stream = fopen(image_path, 'rb')
        content_length = os.path.getsize(image_path)

        return stream, content_length

    def save(self, image):
        uuid = self._uuidgen()

        file_name = '{uuid}.png'.format(uuid=uuid)
        file_path = self.file_path(file_name)

        image.write_to_file(file_path)

        return {
            'type': 'thumbnail',
            'uuid': str(uuid),
            'ext': 'png',
            '$ref': '/api/cache/{uuid}.png'.format(uuid=uuid)
        }

