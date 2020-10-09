# AuthMiddleware.py

import falcon
import jwt

class AuthMiddleware(object):
    def __init__(self, key):
        self._key = key

    def process_request(self, req, resp):
        if req.method == 'OPTIONS':
            return

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

    def _token_is_valid(self, token, req):
        try:
            payload = jwt.decode(token, self._key, algorithms=['HS256'])
            req.context.auth = payload
            return True
        except:
            return False
