# CacheStore.py

import io
import os
import re
import uuid
import mimetypes
import json
import falcon

class CacheStore(object):
    def __init__(self, storage_path, uuidgen=uuid.uuid4, fopen=io.open):
        self._storage_path = storage_path
        self._uuidgen = uuidgen
        self._open = fopen

    def file_path(self, name):
        return os.path.join(self._storage_path, name)

    def read_file(self, name):
        path = self.file_path(name)
        stream = self._open(path, 'rb')
        content_length = os.path.getsize(path)

        return stream, content_length