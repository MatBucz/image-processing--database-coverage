from os import listdir
from os.path import isfile, join, isdir


class ImageIteratorInputError(Exception):
    pass


class ImageIterator:
    def __init__(self, image_collection):
        self._image_collection = image_collection
        self._index = 0

    def __next__(self):
        if self._index < len(self._image_collection.files):
            result = (
                self._image_collection.directory
                + self._image_collection.files[self._index]
            )
            self._index += 1
            return result
        raise StopIteration


class ImageCollection:
    def __init__(self, directory: str):
        if not isdir(directory):
            raise ImageIteratorInputError(
                f"Provided path is not directory '{directory}'"
            )
        self.files = [f for f in listdir(directory) if isfile(join(directory, f))]
        if not len(self.files):
            raise ImageIteratorInputError(
                f"Provided path does not contain files '{directory}'"
            )
        self.directory = directory
        if not self.directory.endswith("/"):
            self.directory += "/"

    def __iter__(self):
        return ImageIterator(self)
