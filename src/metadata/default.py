# default.py

import os
import time

from stat import ST_MTIME, ST_CTIME, ST_SIZE

class default(object):
    def __init__(self, file_path, data):
        st = os.stat(file_path)

        data['metadata']['file'] = {
            'size': str(st[ST_SIZE]),
            'datetime': time.asctime(time.localtime(st[ST_MTIME]))
        }

    def str(self):
        print('default')
