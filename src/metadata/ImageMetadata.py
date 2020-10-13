# ImageMetadata

import imghdr

from PIL import Image, ExifTags

class ImageMetadata(object):
    def __init__(self, file_path, data):
        file_type = imghdr.what(file_path)

        if file_type:
            self.read_metadata(file_path, data)

    def read_metadata(self, file_path, data):
        try:
            imageObject = Image.open(file_path)
            imageSize = imageObject.size
            
            data['metadata'] = {
                'fileFormat': imageObject.format,
                'imageMode': imageObject.mode,
                'imageSize': { 
                    'width': imageSize[0],
                    'height': imageSize[1]
                }
            }

            if imageObject._getexif():
                data['metadata']['exif'] = { }
                for k, v in imageObject._getexif().items():
                    if k in ExifTags.TAGS:
                        if isinstance(v, bytes):
                            d = v.decode('unicode-escape').encode('latin1').decode('utf8')
                            data['metadata']['exif'][ExifTags.TAGS[k]] = d.replace('ASCII\u0000\u0000\u0000', '') 
                        else:
                            data['metadata']['exif'][ExifTags.TAGS[k]] = str(v)
        except Exception as inst:
            print(type(inst))
            print(inst.args)
