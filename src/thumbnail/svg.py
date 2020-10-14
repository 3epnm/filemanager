# svg.py

import os
import uuid
import pyvips

from thumbnail.png import png

class svg(png):
    def str(self):
        print('svg')
