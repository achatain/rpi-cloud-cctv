from google.cloud import storage
import os


class CloudStorageThreadedClient:
    def __init__(self):
        pass

    def list(self, bucket_name):
        print 'attempting to read %s' % bucket_name
        client = storage.Client()
        bucket = client.get_bucket(bucket_name)
        for blob in bucket.list_blobs():
            print blob

    def get(self, bucket_name, file_name):
        client = storage.Client()
        bucket = client.get_bucket(bucket_name)
        blob = bucket.get_blob(file_name)
        file1 = open(file_name, 'w')
        file1.write(blob.download_as_string())
