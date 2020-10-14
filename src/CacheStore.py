# CacheStore.py

import io
import os
import re
import uuid
import mimetypes
import json
import falcon

class CacheStore(object):
    def __init__(self, storage_path, uuidgen=uuid.uuid4):
        self._storage_path = storage_path
        self._uuidgen = uuidgen

    def file_path(self, name):
        return os.path.join(self._storage_path, name)

    def read_file(self, name, fopen=io.open):
        path = self.file_path(name)
        stream = fopen(path, 'rb')
        content_length = os.path.getsize(path)

        return stream, content_length