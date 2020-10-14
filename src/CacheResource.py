# FileResource.py

import io
import falcon
import mimetypes
import json

class CacheResource(object):
    def __init__(self, cache_store):
        self._cache_store = cache_store

    def on_get(self, req, resp, name):
        try:
            resp.content_type = mimetypes.guess_type(name)[0]
            resp.stream, resp.content_length = self._cache_store.read_file(name)
        except IOError:
            raise falcon.HTTPNotFound()

