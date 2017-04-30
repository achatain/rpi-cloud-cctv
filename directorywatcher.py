import logging
from os import listdir
from os.path import isfile
from time import sleep

logger = logging.getLogger(__name__)


def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]


class DirectoryWatcher:
    def __init__(self, directory_to_watch, file_added_callback=None, file_removed_callback=None):
        self.directory_to_watch = directory_to_watch
        self.file_added_callback = file_added_callback
        self.file_removed_callback = file_removed_callback
        logger.info('Initiated DirectoryWatcher')

    def for_each_file_do(self, callback):
        while 1:
            files = listdir(self.directory_to_watch)
            for file_name in files:
                if isfile(self.directory_to_watch + file_name) and not file_name.endswith('.tmp'):
                    callback(self.directory_to_watch, file_name)
            #sleep(1)

    def watch(self):
        current_list = listdir(self.directory_to_watch)

        while 1:
            updated_list = listdir(self.directory_to_watch)

            added = diff(updated_list, current_list)
            removed = diff(current_list, updated_list)

            if added.__len__():
                logger.info('File(s) added %s', added)
                if self.file_added_callback:
                    for filename in added:
                        self.file_added_callback(filename)

            if removed.__len__():
                logger.info('File(s) removed %s', removed)
                if self.file_removed_callback:
                    for filename in removed:
                        self.file_removed_callback(filename)

            current_list = updated_list
            #sleep(1)
