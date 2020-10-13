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
from CacheResource import CacheResource
from FileResource import FileResource
from ThumbnailResource import ThumbnailResource

config = configparser.ConfigParser()
config.read('config.ini')

application = api = falcon.API(middleware=[
    AuthMiddleware(config['jwt']['key']),
    MultipartMiddleware(),
    CORSMiddleware()
])

databaseService = DatabaseService(config['database']['connect_string'])

versionResource = VersionResource()

fileStore = FileStore(config['storage']['data'], databaseService)
fileResource = FileResource(fileStore)

cacheStore = CacheStore(config['storage']['cache'])
cacheResource = CacheResource(cacheStore)
thumbnailResource = ThumbnailResource(fileStore, cacheStore)

api.add_route('/api/version', versionResource)
api.add_route('/api/file', fileResource)
api.add_route('/api/file/{name}', fileResource)
api.add_route('/api/thumbnail/{name}', thumbnailResource)
api.add_route('/api/cache/{name}', cacheResource)

