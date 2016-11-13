from config import huey
from config import mongo
import exifextractor

@huey.task()
def process_photo(base_url, key):
    """
    Calls exifextractor.process_photo as a Huey task.
    """
    exifextractor.process_photo(base_url, key, mongo=mongo)
