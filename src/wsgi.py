import os
import falcon
import configparser

from falcon_multipart.middleware import MultipartMiddleware
from CORSMiddleware import CORSMiddleware
from AuthMiddleware import AuthMiddleware

from DatabaseService import DatabaseService
from VersionResource import VersionResource
from FileStore import FileStore
from CacheStore import CacheStore
from FileResource import FileResource
from CacheResource import CacheResource
from ThumbnailResource import ThumbnailResource

config = configparser.ConfigParser()
config.read('config.ini')

application = api = falcon.API(middleware=[
    AuthMiddleware(config['jwt']['key'], False),
    MultipartMiddleware(),
    CORSMiddleware()
])

# databaseService = DatabaseService(config['database']['connect_string'])

versionResource = VersionResource()

fileStore = FileStore(config['storage']['path'], None)
cacheStore = CacheStore(config['storage']['path'])

fileResource = FileResource(fileStore)
cacheResource = CacheResource(cacheStore)
thumbnailResource = ThumbnailResource(fileStore, cacheStore)

api.add_route('/api/version', versionResource)
api.add_route('/api/file', fileResource)
api.add_route('/api/file/{name}', fileResource)
api.add_route('/api/cache/{name}', cacheResource)
api.add_route('/api/thumbnail/{name}', thumbnailResource)
