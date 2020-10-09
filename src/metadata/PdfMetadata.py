# PdfMetadata.ty

import PyPDF2

class PdfMetadata(object):
    def __init__(self, file_path, data):
        self.read_metadata(file_path, data)

    def read_metadata(self, file_path, data):
        try:
            pdf = PyPDF2.PdfFileReader(open(file_path, "rb"))
            info = pdf.getDocumentInfo()
            pages = pdf.getNumPages()

            data['metadata'] = {
                'pages': pages,
                'author': info.author,
                'creator': info.creator,
                'producer': info.producer,
                'subject': info.subject,
                'title': info.title
            }
        except PyPDF2.utils.PdfReadError:
            print('no pdf')
        else:
            pass

