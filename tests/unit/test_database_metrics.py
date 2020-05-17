from unittest import TestCase

from app.database_metrics import DatabaseMetrics, DatabaseMetricsError


class TestDatabaseMetrics(TestCase):
    def test_should_plot_all(self):
        dm = DatabaseMetrics("tests/assets/test_db", None, (100, 100), "test_db")
        dm.plot_all()

    def test_should_raise_on_missing_dir(self):
        with self.assertRaises(DatabaseMetricsError):
            DatabaseMetrics("missing", None, "test_db")
