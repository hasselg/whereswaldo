
from gevent import monkey; monkey.patch_all()

from io import BytesIO
import exifread
import requests
import config

def process_photo(base_url, key, mongo=config.local_mongo):
    """
    Retrieves the photo located at base_url/key and extracts the exif data from
    it. The extracted exif data is then inserted into the MongoDB collection
    referenced by mongo.
    """
    url = base_url + key
    r = requests.get(url)

    if r.status_code == 200:
        exif_doc = {'id': key}
        tags = exifread.process_file(BytesIO(r.content), details=False)

        # Not every photo will have EXIF data. Only convert keys if EXIF data
        # was present
        if tags is not None and len(tags.keys()) > 0:
            for tag in tags.keys():
                exif_doc[tag] = str(tags[tag])

        mongo.insert(exif_doc)
        print("key {} processed".format(key))
    else:
        print("Failed to download img at {}".format(url))
