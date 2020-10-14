# pdf.py

import PyPDF2

class pdf(object):
    def __init__(self, file_path, data):
        try:
            pdf = PyPDF2.PdfFileReader(open(file_path, "rb"))
            info = pdf.getDocumentInfo()
            pages = pdf.getNumPages()

            data['metadata']['pdf'] = {
                'pages': pages,
                'author': info.author,
                'creator': info.creator,
                'producer': info.producer,
                'subject': info.subject,
                'title': info.title
            }
        except Exception as inst:
            print(type(inst))
            print(inst.args)
