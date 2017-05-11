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
import constants
from os import listdir
from os.path import isfile
from time import sleep

logger = logging.getLogger(__name__)


def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]


class DirectoryWatcher(object):
    """
    Class for monitoring a directory for files creation and triggering callbacks whenever the latter happens.
    """

    def __init__(self, directory_to_watch, file_added_callback=None, file_removed_callback=None):
        """
        :param str directory_to_watch:
            The directory to be monitored
        
        :param method file_added_callback:
            The method to call back whenever a file is added into the monitored directory
        """
        self.directory_to_watch = directory_to_watch
        self.file_added_callback = file_added_callback
        self.file_removed_callback = file_removed_callback
        logger.info('Initiated DirectoryWatcher')

    def for_each_file_do(self, callback):
        while 1:
            logger.debug('List files in dir %s', self.directory_to_watch)
            files = listdir(self.directory_to_watch)
            for file_name in files:
                logger.debug('Found file with name %s', file_name)
                if isfile(self.directory_to_watch + file_name) and file_name.endswith(constants.file_video_extension):
                    logger.debug('File with name %s eligible for callback %s', file_name, callback)
                    callback(self.directory_to_watch, file_name)
                else:
                    logger.debug('File with name %s not eligible for callback', file_name)
            sleep(1)

    def watch(self):
        current_list = listdir(self.directory_to_watch)

        while 1:
            updated_list = listdir(self.directory_to_watch)

            added = diff(updated_list, current_list)
            removed = diff(current_list, updated_list)

            if len(added):
                logger.info('File(s) added %s', added)
                if self.file_added_callback:
                    for filename in added:
                        self.file_added_callback(filename)

            if len(removed):
                logger.info('File(s) removed %s', removed)
                if self.file_removed_callback:
                    for filename in removed:
                        self.file_removed_callback(filename)

            current_list = updated_list
            sleep(1)
