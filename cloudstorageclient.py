# https://github.com/achatain/rpi-cloud-cctv
#
# Copyright (C) 2017 Antoine Chatain (achatain [at] outlook [dot] com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import logging
import os
from google.cloud import storage
from google.cloud.exceptions import GoogleCloudError

logger = logging.getLogger(__name__)


class CloudStorageClient(object):
    """
    Client for interacting with Google Cloud Storage.
    """

    def __init__(self, bucket_name):
        """
        :param str bucket_name:
            The name of the Google Cloud Storage bucket the instance points to.
        """
        self.bucket_name = bucket_name
        logger.info('Initiated CloudStorageClient')

    def upload(self, directory, file_name):
        """
        Upload a file to the Google Cloud Storage the instance is pointing at. Upon successful upload, the local
        file copy is deleted.
        :param str directory:
            The directory holding the file to upload
        
        :param str file_name:
            The name of the file to upload
        """
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
        local_file.close()
