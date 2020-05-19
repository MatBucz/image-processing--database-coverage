from unittest import TestCase

from app.database_analyze import DatabaseAnalyze


class TestImageCollection(TestCase):
    def test_should_perform_analysis_and_fills_dataframe(self):
        da = DatabaseAnalyze("tests/assets/")
        da.analyze()
        self.assertGreater(da.df.size, 0)
