# FileResource.py

import io
import falcon
import mimetypes
import json

class FileResource(object):
    def __init__(self, file_store):
        self._file_store = file_store

    def on_get(self, req, resp, name):
        resp.content_type = mimetypes.guess_type(name)[0]
        resp.stream, resp.content_length = self._file_store.open_file(name)

    def on_post(self, req, resp):
        doc = self._file_store.save(req.get_param('file'), req.context.auth['userid'])

        resp.body = json.dumps(doc)
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_200