import logging
import os
from google.cloud import storage
from google.cloud.exceptions import GoogleCloudError

logger = logging.getLogger(__name__)


class CloudStorageClient:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        logger.info('Initiated CloudStorageClient')

    def upload(self, directory, file_name):
        client = storage.Client()
        bucket = client.get_bucket(self.bucket_name)
        blob = bucket.blob(file_name)
        path = directory + file_name
        try:
            logger.info('Started uploading file %s ...', path)
            blob.upload_from_filename(path)
        except (ValueError, GoogleCloudError) as ex:
            logger.error('Unable to upload file %s%s [%s]', directory, file_name, ex)
        else:
            logger.info('Successfully uploaded file %s%s and deleted local copy', directory, file_name)
            os.remove(path)

    def list(self):
        logger.info('attempting to list blobs from %s', self.bucket_name)
        client = storage.Client()
        bucket = client.get_bucket(self.bucket_name)
        for blob in bucket.list_blobs():
            logger.info(blob)

    def get(self, file_name):
        client = storage.Client()
        bucket = client.get_bucket(self.bucket_name)
        blob = bucket.get_blob(file_name)
        local_file = open(file_name, 'w')
        local_file.write(blob.download_as_string())
