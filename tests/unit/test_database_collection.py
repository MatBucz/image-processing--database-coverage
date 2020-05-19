from unittest import TestCase

# fmt: off
from app.database_collection import (DatabaseCollection,
                                     DatabaseIteratorInputError)

# fmt: on


class TestDatabaseCollection(TestCase):
    def test_should_create_collection(self):
        dc = DatabaseCollection("tests/assets/")
        expected_dbs = [
            "test_db",
            "test_db2",
        ]
        db_list = [database for database in dc]
        self.assertCountEqual(db_list, expected_dbs)

    def test_should_raise_exception_on_wrong_dir(self):
        with self.assertRaises(DatabaseIteratorInputError):
            DatabaseCollection("missing")
