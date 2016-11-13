"""
This module is a sanity check, running the same batch photo processing as
the publisher module, but not farming the tasks out via Huey and is single
threaded.
"""
import time

import boto3
from botocore import UNSIGNED
from botocore.client import Config
from botocore.exceptions import ClientError

from exifextractor import process_photo
from publisher import Publisher

def main():
    p = Publisher()
    p.publish_items_from_bucket()

if __name__ == '__main__':
    start = time.perf_counter()
    main()
    stop = time.perf_counter()

    print("elapsed clock publishing/processing time: {}".format(stop - start))
