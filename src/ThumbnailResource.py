# ThumbnailResource.py

import os
import imp
import falcon
import mimetypes
import json
import pyvips

from thumbnail.default import default

class ThumbnailResource(object):
    def __init__(self, file_store, cache_store):
        self._file_store = file_store
        self._cache_store = cache_store

    def on_get(self, req, resp, name):
        metadata = self._file_store.read_json(name)
        thumb = next((x for x in metadata['links'] if x['type'] == 'thumbnail'), None)

        if not thumb:
            uuid = metadata['uuid']
            ext = self._file_store.get_ext(metadata['type'], metadata['name'])

            name = '{uuid}{ext}'.format(uuid=uuid, ext=ext)
            file = self._file_store.file_path(name)
            
            module_path = os.path.join(os.path.dirname(__file__), 'thumbnail')
            module_name = ext[1:]
            try:  
                fp, path, desc = imp.find_module(module_name, [ module_path ])
                package = imp.load_module(module_name, fp, path, desc)

                image = getattr(package, module_name)(self._cache_store)
                thumb = image.create(file)
            except ImportError: 
                image = default(self._cache_store)
                thumb = image.create(ext)

            metadata['links'].append(thumb)

            self._file_store.write_json(metadata)

        resp.content_type = 'image/png'
        name = '{uuid}.png'.format(uuid=thumb['uuid'])
        resp.stream, resp.content_length = self._cache_store.read_file(name)
