import os
import logging
from cloudstoragethreadedclient import CloudStorageThreadedClient

BUCKET_ENV = 'RPI_CLOUD_CCTV_BUCKET'


def main():
    init_logging()
    init_config()
    # client = CloudStorageThreadedClient()
    # client.list(os.getenv('RPI_CLOUD_CCTV_BUCKET'))
    logging.info('Finished rpi-cloud-cctv app')


def init_logging():
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', filename='rpicloudcctv.log', level=logging.INFO)
    logging.info('Started rpi-cloud-cctv app')


def init_config():
    if os.getenv(BUCKET_ENV) is None:
        print '%s env variable should be set' % BUCKET_ENV
        exit(1)


if __name__ == '__main__':
    main()
