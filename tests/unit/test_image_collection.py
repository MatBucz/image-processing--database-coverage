from unittest import TestCase

from app.image_collection import ImageCollection, ImageIteratorInputError


class TestImageCollection(TestCase):
    def test_should_create_collection(self):
        ic = ImageCollection("tests/assets/test_db")
        expected_images = [
            "tests/assets/test_db/fruits.png",
            "tests/assets/test_db/lena.png",
        ]
        image_list = [img for img in ic]
        self.assertCountEqual(image_list, expected_images)

    def test_should_raise_exception_on_wrong_dir(self):
        with self.assertRaises(ImageIteratorInputError):
            ImageCollection("missing")
