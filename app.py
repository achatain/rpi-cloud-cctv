import os
from cloudstoragethreadedclient import CloudStorageThreadedClient

BUCKET_ENV = 'RPI_CLOUD_CCTV_BUCKET'

if os.getenv(BUCKET_ENV) is None:
    print '%s env variable should be set' % BUCKET_ENV
    exit(1)

client = CloudStorageThreadedClient()
client.list(os.getenv('RPI_CLOUD_CCTV_BUCKET'))
