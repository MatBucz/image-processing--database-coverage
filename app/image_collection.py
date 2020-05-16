"""Tools for handling multiple images in the DB"""

from os import listdir
from os.path import isfile, join, isdir


class ImageIteratorInputError(Exception):
    """Image Iterator Error raised on wrong input params"""


class ImageIterator:
    """Iterator class for getting all images"""

    def __init__(self, image_collection) -> None:
        """Iterator init"""
        self._image_collection = image_collection
        self._index = 0

    def __next__(self) -> str:
        """
        Next image
        :return: filename with path of the DB
        """
        if self._index < len(self._image_collection.files):
            result = (
                self._image_collection.directory
                + self._image_collection.files[self._index]
            )
            self._index += 1
            return result
        raise StopIteration


class ImageCollection:
    """Collection of images in the database based on iterator"""

    def __init__(self, directory: str) -> None:
        """
        Create image collection
        :param directory: path to the DB directory
        """
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

    def __iter__(self) -> ImageIterator:
        """
        Iterator
        :return: Image iterator
        """
        return ImageIterator(self)
