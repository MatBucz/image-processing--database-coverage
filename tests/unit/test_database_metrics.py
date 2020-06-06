from unittest import TestCase

from app.database_metrics import DatabaseMetrics, DatabaseMetricsError


class TestDatabaseMetrics(TestCase):
    def setUp(self) -> None:
        self.dm = DatabaseMetrics(
            "tests/assets/test_db", None, (112.02, 85.83), "test db"
        )

    def test_should_plot_all(self):
        self.dm.plot_all()

    def test_should_calculate_si_and_cf_ranges(self):
        si, cf = self.dm.get_si_cf_ranges()
        self.assertGreaterEqual(si, 0.0)
        self.assertLessEqual(si, 1.0)
        self.assertGreaterEqual(cf, 0.0)
        self.assertLessEqual(cf, 1.0)

    def test_should_calculate_convex_hull_area(self):
        area = self.dm.get_coverage_area()
        self.assertGreaterEqual(area, 0.0)
        self.assertLessEqual(area, 1.0)

    def test_should_calculate_fill_rate(self):
        fill_rate = self.dm.calculate_fill_rate_fixed_radius_area()
        self.assertGreaterEqual(fill_rate, 0.0)
        self.assertLessEqual(fill_rate, 1.0)

    def test_should_get_info(self):
        db_info = self.dm.info()
        self.assertIsInstance(db_info, dict)

    def test_should_raise_on_missing_dir(self):
        with self.assertRaises(DatabaseMetricsError):
            DatabaseMetrics("missing", None, (100, 100), "test_db")
