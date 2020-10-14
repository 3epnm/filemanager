# gif.py

import os
import uuid

from shutil import copyfile
from thumbnail.default import default

class gif(default):
    def create(self, read_file):
        uuid, name, write_file = self.write_file_path()

        copyfile(read_file, write_file)

        return {
            'type': 'thumbnail',
            'mime': 'image/gif',
            'uuid': uuid,
            'ext': 'gif',
            '$ref': '/api/cache/{name}'.format(name=name)
        }

    def str(self):
        print('gif')
