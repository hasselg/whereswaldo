from huey import RedisHuey
import pymongo

# Configure Huey
huey = RedisHuey('exifextractor', host='redishost')

# Configure remote and local Mongo collection handle
mongo = pymongo.MongoClient('mongo', 27017)['exifextractor']['photos']
local_mongo = pymongo.MongoClient('localhost', 27017)['exifextractor']['photos']
