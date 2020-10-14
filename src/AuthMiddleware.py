# AuthMiddleware.py

import falcon
import jwt

class AuthMiddleware(object):
    def __init__(self, key, active=True):
        self._key = key
        self._is_active = active

    def process_request(self, req, resp):
        if req.method == 'OPTIONS':
            return

        if not self._is_active:
            self.dummy_request(req, resp)
        else:
            self.do_request(req, resp)

    def do_request(self, req, resp):
        token = req.get_header('Authorization') 

        if req.has_param('token'):
            token = 'Bearer ' + req.get_param('token')

        if token is None:
            description = ('Please provide an auth token '
                        'as part of the request.')

            raise falcon.HTTPUnauthorized('Auth token required',
                                        description)

        if not self._token_is_valid(token[7:], req):
            description = ('The provided auth token is not valid. '
                        'Please request a new token and try again.')

            raise falcon.HTTPUnauthorized('Authentication required',
                                        description)

    def dummy_request(self, req, resp):
        req.context.auth = {
            'context': {
                'user': {
                    'name': 'foobar'
                }
            },
            'userid': 1234,
            'sessionid': 5678
        }

    def _token_is_valid(self, token, req):
        try:
            payload = jwt.decode(token, self._key, algorithms=['HS256'])
            req.context.auth = payload
            return True
        except:
            return False
