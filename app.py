#! /usr/bin/env python2

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


import os
import logging
import threading
import constants
from cloudstorageclient import CloudStorageClient
from directorywatcher import DirectoryWatcher
from rpicamera import RpiCamera


def main():
    init_logging()
    check_config()

    create_directory_watcher_thread().start()
    create_rpi_camera_thread().start()

    while 1:
        pass


def init_logging():
    logging.basicConfig(format=constants.log_format, filename=constants.log_file_name, level=logging.INFO)
    logging.info('Started rpi-cloud-cctv app')


def create_directory_watcher_thread():
    client = CloudStorageClient(os.getenv(constants.env_gcloud_bucket))
    dw = DirectoryWatcher(os.getenv(constants.env_video_dir))
    dw_thread = threading.Thread(target=dw.for_each_file_do, args=(client.upload,))
    dw_thread.setDaemon(True)
    return dw_thread


def create_rpi_camera_thread():
    rpi_camera = RpiCamera(os.getenv(constants.env_video_dir))
    rpi_camera_thread = threading.Thread(target=rpi_camera.run)
    rpi_camera_thread.setDaemon(True)
    return rpi_camera_thread


def check_config():
    for env in constants.required_envs.values():
        if os.getenv(env) is None:
            logging.error('%s env variable is not set', env)
            exit(1)


if __name__ == '__main__':
    main()
