# ThumbnailResource.py

import falcon
import mimetypes
import json
import pyvips

class ThumbnailResource(object):
    def __init__(self, file_store, cache_store):
        self._file_store = file_store
        self._cache_store = cache_store

    def on_get(self, req, resp, name):
        metadata = self._file_store.read_metadata(name)

        thumb = next((x for x in metadata['links'] if x['type'] == 'thumbnail'), None)

        if not thumb:
            data = next(x for x in metadata['links'] if x['type'] == 'file')
            name = '{uuid}.{ext}'.format(uuid=metadata['id'], ext=data['ext'])

            file_path = self._file_store.file_path(name)
            image = pyvips.Image.thumbnail(file_path, 150)

            thumb = self._cache_store.save(image)
            metadata['links'].append(thumb)

            self._file_store.save_json(metadata['id'], metadata)

        resp.content_type = 'image/png'
        name = '{uuid}.png'.format(uuid=thumb['uuid'])
        resp.stream, resp.content_length = self._cache_store.open_file(name)
