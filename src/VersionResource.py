# VersionResource.py

import falcon
import datetime
import json

class VersionResource(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200

        doc = {
            'FileMgr': 'v0.3',
            'DateTime': str(datetime.datetime.now())
        }

        if req.context.auth: 
            doc['Auth'] = {
                'User': req.context.auth['context']['user']['name'],
                'UserId': req.context.auth['userid'],
                "SessionId": req.context.auth['sessionid']
            }
        
        resp.body = json.dumps(doc, ensure_ascii=False)
