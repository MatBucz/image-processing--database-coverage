from unittest import TestCase

from app.image_metrics import ImageMetrics, ImageMetricsInputError


class TestImageMetrics(TestCase):
    def test_should_calculate_si_cf(self):
        expected_si = 65.51
        expected_cf = 76.16
        im = ImageMetrics("tests/assets/fruits.png")
        si, cf = im.calculate_si_cf()
        self.assertAlmostEqual(si, expected_si, 2)
        self.assertAlmostEqual(cf, expected_cf, 2)

    def test_should_raise_exception_on_missing_image(self):
        with self.assertRaises(ImageMetricsInputError):
            ImageMetrics("missing")
