# png.py

import os
import uuid
import pyvips

from thumbnail.default import default

class png(default):
    def create(self, read_file):
        uuid, name, write_file = self.write_file_path()

        image = pyvips.Image.thumbnail(read_file, 210)
        image.write_to_file(write_file)

        return {
            'type': 'thumbnail',
            'mime': 'image/png',
            'uuid': uuid,
            'ext': 'png',
            '$ref': '/api/cache/{name}'.format(name=name)
        }

    def str(self):
        print('png')
