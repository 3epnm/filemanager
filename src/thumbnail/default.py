# default.py

import os
import uuid
import pyvips

class default(object):
    def __init__(self, cache_store, vips=pyvips, uuidgen=uuid.uuid4):
        self._cache_store = cache_store
        self._uuidgen = uuidgen
        self._vips = vips

    def write_file_path(self): 
        uuid = str(self._uuidgen())
        ext = 'png'
        name = '{uuid}.{ext}'.format(uuid=uuid, ext=ext)
        return uuid, name, self._cache_store.file_path(name)

    def create(self, text):
        uuid, name, write_file = self.write_file_path()

        src = b"""<svg xmlns="http://www.w3.org/2000/svg" width="210" height="297">
            <path fill="#f9f9f9" d="M0 0h210v297H0z" />
                <text text-anchor="middle" alignment-baseline="central" style="line-height:1.25" font-size="90" font-family="sans-serif">
                <tspan x="105" dy="177">%s</tspan>
                </text>
            </svg>""" % text.encode('ascii')

        image = self._vips.Image.svgload_buffer(src)
        image.write_to_file(write_file)

        return {
            'type': 'thumbnail',
            'mime': 'image/png',
            'uuid': uuid,
            'ext': 'png',
            '$ref': '/api/cache/{name}'.format(name=name)
        }

    def str(self):
        print('default')
