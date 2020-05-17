"""Tools for calculating metrics for multiple DBs"""
import logging
import os
from typing import Dict

from app.database_collection import DatabaseCollection
from app.database_metrics import DatabaseMetrics
from matplotlib import pyplot as plt


class DatabaseAnalyzeError(Exception):
    """Generic DatabaseAnalyze Error"""


class DatabaseAnalyze:
    def __init__(self, parent_dir: str, output: str):
        logging.debug(
            f"DatabaseAnalyze init for dir: '{parent_dir}' and output: '{output}'"
        )
        self.parent_dir = parent_dir
        self.output = output

        self.max_si = 0.0
        self.max_cf = 0.0

        if not os.path.isdir(self.parent_dir):
            raise DatabaseAnalyzeError(
                f"Given path '{self.parent_dir}' is not valid directory"
            )
        self.dc = DatabaseCollection(self.parent_dir)

        self.db_metric: Dict[str, DatabaseMetrics] = dict()

        self.__get_max_si_cf()
        logging.debug(f"Max SI: '{self.max_si}', Max CF: '{self.max_cf}'")

    def __get_max_si_cf(self) -> None:
        """
        Iterates over all databases and calculate max SI and CF across all DBs
        """
        for db in self.dc:
            db_metric = DatabaseMetrics(
                self.parent_dir + db, self.output, (1.0, 1.0), db
            )
            si, cf = db_metric.get_max_si_cf()
            self.max_si = si if si > self.max_si else self.max_si
            self.max_cf = cf if cf > self.max_cf else self.max_cf

    def analyze(self):
        for db in self.dc:
            self.db_metric[db] = DatabaseMetrics(
                self.parent_dir + db, self.output, (self.max_si, self.max_cf), db
            )
        self.__relative_ranges()

    def __relative_ranges(self):
        si_rr: Dict[str, float] = dict()
        cf_rr: Dict[str, float] = dict()
        for db in self.dc:
            si_rr[db], cf_rr[db] = self.db_metric[db].get_si_cf_ranges()
        plt.bar(range(len(si_rr)), list(si_rr.values()), align="center")
        plt.xticks(range(len(si_rr)), list(si_rr.keys()))
        plt.show()