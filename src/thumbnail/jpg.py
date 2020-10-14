# jpg.py

import os
import uuid
import pyvips

from thumbnail.png import png

class jpg(png):
    def str(self):
        print('jpg')
