"""Tools for handling multiple DBs"""

from os import listdir
from os.path import isdir, join


class DatabaseIteratorInputError(Exception):
    """Database Iterator Error raised on wrong input params"""


class DatabaseIterator:
    """Iterator class for getting all databases"""

    def __init__(self, database_collection) -> None:
        """Iterator init"""
        self._database_collection = database_collection
        self._index = 0

    def __next__(self) -> str:
        """
        Next database
        :return: path to the DB
        """
        if self._index < len(self._database_collection.dirs):
            result = self._database_collection.dirs[self._index]
            self._index += 1
            return result
        raise StopIteration


class DatabaseCollection:
    """Collection of the databases based on iterator"""

    def __init__(self, directory: str) -> None:
        """
        Creates database collection
        :param directory: path to the parent directory of multiple DBs
        """
        if not isdir(directory):
            raise DatabaseIteratorInputError(
                f"Provided path is not directory '{directory}'"
            )
        self.dirs = [f for f in listdir(directory) if isdir(join(directory, f))]
        if not len(self.dirs):
            raise DatabaseIteratorInputError(
                f"Provided path does not contain directories '{directory}'"
            )
        self.parent_directory = directory
        if not self.parent_directory.endswith("/"):
            self.parent_directory += "/"

    def __iter__(self) -> DatabaseIterator:
        """
        Iterator
        :return: Database iterator
        """
        return DatabaseIterator(self)
