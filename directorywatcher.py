from os import listdir
from time import sleep


def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]


class DirectoryWatcher:
    def __init__(self, directory_to_watch, file_added_callback=None, file_removed_callback=None):
        self.directoryToWatch = directory_to_watch
        self.file_added_callback = file_added_callback
        self.file_removed_callback = file_removed_callback

    def watch(self):
        current_list = listdir(self.directoryToWatch)

        while True:
            updated_list = listdir(self.directoryToWatch)

            added = diff(updated_list, current_list)
            removed = diff(current_list, updated_list)

            if added.__len__():
                print 'File(s) added %s' % added
                if self.file_added_callback:
                    for filename in added:
                        self.file_added_callback(filename)

            if removed.__len__():
                print 'File(s) removed %s' % removed
                if self.file_removed_callback:
                    for filename in removed:
                        self.file_removed_callback(filename)

            current_list = updated_list
            sleep(1)
