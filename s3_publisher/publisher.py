import time

import boto3
from botocore import UNSIGNED
from botocore.client import Config
from botocore.exceptions import ClientError

from config import huey
import exifextractor
import exifextractortask
from huey.consumer import EVENT_FINISHED
from huey.consumer import EVENT_ERROR_TASK

class Publisher:
    def __init__(self, bucket_name="waldo-recruiting", limit=None,
        process_photo_func=exifextractor.process_photo):
        """
        A publisher that consumes a list of photo URLs from an Amazon S3 bucket
        named bucket_name and processes them through the process_photo_func.
        """
        self._bucket_name = bucket_name
        self._limit = limit
        self._process_photo_func = process_photo_func
        self._s3_base_url = "http://s3.amazonaws.com/" + self._bucket_name + "/"
        self.pub_count = 0

        # Setup our low-level client for unsigned access
        self._s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

        # Check that the bucket exists
        try:
            request = self._s3.head_bucket(Bucket=bucket_name)
        except ClientError as ce:
            raise RuntimeError("Unable to access bucket [{}]"
                .format(bucket_name)).with_traceback(ce)

    def _process_records(self, records):
        for record in records:
            key = record['Key']
            self._process_photo_func(self._s3_base_url, key)
            self.pub_count += 1

            # If we've hit the maximum number of photos to process, bail out!
            if self._limit is not None and self.pub_count >= self._limit:
                break

    def publish_items_from_bucket(self):
        """
        Consumes the URLs from @self._bucket_name and submits them to
        @self._process_photo_func.
        """
        # Get our initial list of objects from the bucket
        response = self._s3.list_objects_v2(Bucket=self._bucket_name)

        while True and response is not None:
            records = response['Contents']
            self._process_records(records)

            # If we didn't get all of the objects back in our list, request
            # the rest from AWS
            if response['IsTruncated'] is True:
                token = response['NextContinuationToken']
                response = self._s3.list_objects_v2(Bucket=self._bucket_name,
                    ContinuationToken=token)
            else:
                break

def main():
    # Instantiate our publisher and begin publishing
    p = Publisher(process_photo_func=exifextractortask.process_photo)
    p.publish_items_from_bucket()
    print("published {} items".format(p.pub_count))

    # Count the completed events so we know when we can stop listening for
    # more events and exit
    events_ok = 0
    events_errored = 0
    for event in huey.storage:
        if event['status'] == EVENT_FINISHED:
            last_event_time = time.time()
            events_ok += 1
        elif event['status'] == EVENT_ERROR_TASK:
            events_errored += 1

        event_count = events_ok + events_errored
        if event_count >= p.pub_count:
            break
        else:
            print("event count: {}".format(event_count))

if __name__ == '__main__':
    start = time.perf_counter()
    main()
    stop = time.perf_counter()
    print("elapsed clock publishing/processing time: {}".format(stop - start))
