import os
import logging
import threading
from cloudstorageclient import CloudStorageClient
from directorywatcher import DirectoryWatcher
from rpicamera import RpiCamera

required_envs = {
    'video_dir': 'RPI_CLOUD_CCTV_VIDEO_DIR',
    'gcloud_bucket': 'RPI_CLOUD_CCTV_BUCKET',
    'gcloud_credentials': 'GOOGLE_APPLICATION_CREDENTIALS'
}


def main():
    init_logging()
    check_config()

    # This will monitor the directory where videos are stored and upload each video file to the cloud
    client = CloudStorageClient(os.getenv(required_envs['gcloud_bucket']))
    dw = DirectoryWatcher(os.getenv(required_envs['video_dir']))
    dw_thread = threading.Thread(target=dw.for_each_file_do, args=(client.upload,))
    dw_thread.setDaemon(True)

    rpi_camera = RpiCamera(os.getenv(required_envs['video_dir']))
    rpi_camera_thread = threading.Thread(target=rpi_camera.run)
    rpi_camera_thread.setDaemon(True)

    dw_thread.start()
    rpi_camera_thread.start()

    while 1:
        pass


def init_logging():
    logging.basicConfig(format='%(asctime)s %(levelname)s [%(name)s] %(message)s', filename='rpicloudcctv.log',
                        level=logging.INFO)
    logging.info('Started rpi-cloud-cctv app')


def check_config():
    for env in required_envs.values():
        if os.getenv(env) is None:
            logging.error('%s env variable is not set', env)
            exit(1)


if __name__ == '__main__':
    main()
