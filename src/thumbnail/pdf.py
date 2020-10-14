# pdf.py

import os
import uuid
import pyvips

from thumbnail.png import png

class pdf(png):
    def str(self):
        print('pdf')
