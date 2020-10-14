# image.py

import imghdr

from PIL import Image, ExifTags

class image(object):
    def __init__(self, file_path, data):
        file_type = imghdr.what(file_path)

        if file_type:
            try:
                imageObject = Image.open(file_path)
                imageSize = imageObject.size
                
                data['metadata']['image'] = {
                    'fileFormat': imageObject.format,
                    'imageMode': imageObject.mode,
                    'imageWidth': imageSize[0],
                    'imageHeight': imageSize[1]
                }

                if imageObject._getexif():
                    data['metadata']['image']['exif'] = { }
                    for k, v in imageObject._getexif().items():
                        if k in ExifTags.TAGS:
                            if isinstance(v, bytes):
                                d = v.decode('unicode-escape').encode('latin1').decode('utf8')
                                data['metadata']['image']['exif'][ExifTags.TAGS[k]] = d.replace('ASCII\u0000\u0000\u0000', '') 
                            elif isinstance(v, int):
                                data['metadata']['image']['exif'][ExifTags.TAGS[k]] = v
                            else:
                                data['metadata']['image']['exif'][ExifTags.TAGS[k]] = str(v)
            except Exception as inst:
                print(type(inst))
                print(inst.args)