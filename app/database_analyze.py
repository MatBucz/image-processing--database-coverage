"""Tools for calculating metrics for multiple DBs"""
import logging
import os
from typing import Dict, Optional

import pandas as pd
import seaborn as sns
from app.database_collection import DatabaseCollection
from app.database_metrics import DatabaseMetrics
from matplotlib import pyplot as plt
from matplotlib import rc
from scipy.stats import entropy


class DatabaseAnalyzeError(Exception):
    """Generic DatabaseAnalyze Error"""


class DatabaseAnalyze:
    def __init__(self, parent_dir: str, output: Optional[str] = None):
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

        self.df = pd.DataFrame(
            columns=[
                "Uniformity",
                "Relative ranges",
                "Metric",
                "Database",
                "Area",
                "Fill rate",
                "Distorted images",
                "Distortion types",
                "Distortion levels",
                "Applied distortions",
                "Year",
            ]
        )

        self.__get_max_si_cf()
        logging.debug(f"Max SI: '{self.max_si}', Max CF: '{self.max_cf}'")

        sns.set(style="white")
        rc("font", **{"size": 36, "family": "serif", "serif": ["Computer Modern"]})
        rc("text", usetex=True)

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

    def analyze(self) -> None:
        """
        Main entrypoint for performing analysis
        """
        for db in self.dc:
            self.db_metric[db] = DatabaseMetrics(
                self.parent_dir + db, self.output, (self.max_si, self.max_cf), db
            )
            self.db_metric[db].plot_all()
        self.__parse_info()
        self.__fill_rate_factor()
        self.__uniformity()
        self.__relative_ranges()
        self.__convex_hull_area()

    def __parse_info(self):
        for db in self.dc:
            info = self.db_metric[db].info()
            self.df = self.df.append(
                {
                    "Year": info["year"],
                    "Distorted images": info["distorted_images"],
                    "Distortion types": info["distortion_types"],
                    "Distortion levels": info["distortion_levels"],
                    "Applied distortions": info["applied_distortion"],
                    "Database": db,
                },
                ignore_index=True,
            )
        for metric in (
            "Distorted images",
            "Distortion types",
            "Distortion levels",
            "Applied distortions",
        ):
            self.__single_bar(metric, False)

    def __relative_ranges(self):
        for db in self.dc:
            si_rr, cf_rr = self.db_metric[db].get_si_cf_ranges()
            self.df = self.df.append(
                {"Relative ranges": si_rr, "Metric": "SI", "Database": db},
                ignore_index=True,
            )
            self.df = self.df.append(
                {"Relative ranges": cf_rr, "Metric": "CF", "Database": db},
                ignore_index=True,
            )
        self.__double_bar("Relative ranges")

    def __convex_hull_area(self):
        for db in self.dc:
            area = self.db_metric[db].get_coverage_area()
            self.df = self.df.append({"Area": area, "Database": db}, ignore_index=True)
        self.__single_bar("Area")

    def __fill_rate_factor(self):
        for db in self.dc:
            fill_rate = self.db_metric[db].calculate_fill_rate_fixed_radius_area()
            self.df = self.df.append(
                {"Fill rate": fill_rate, "Database": db}, ignore_index=True
            )
        self.__single_bar("Fill rate")

    def __uniformity(self):
        for db in self.dc:
            si_uni = entropy(self.db_metric[db].si, base=10)
            cf_uni = entropy(self.db_metric[db].cf, base=10)
            self.df = self.df.append(
                {"Uniformity": si_uni, "Metric": "SI", "Database": db},
                ignore_index=True,
            )
            self.df = self.df.append(
                {"Uniformity": cf_uni, "Metric": "CF", "Database": db},
                ignore_index=True,
            )
        self.__double_bar("Uniformity")

    def __single_bar(self, y, unit_scale: bool = True):
        plt.clf()
        self.df = self.df.sort_values(by=y, ascending=False)
        ax = sns.barplot(x="Database", y=y, data=self.df)
        if unit_scale:
            plt.ylim(0, 1)
        plt.ylabel(None)
        plt.title(y)
        if self.output is not None:
            fig = ax.get_figure()
            fig.savefig(self.output + f"{y}.png")

    def __double_bar(self, y):
        plt.clf()
        self.df = self.df.sort_values(by=y, ascending=False)
        ax = sns.barplot(x="Database", y=y, hue="Metric", data=self.df)
        plt.ylim(0, 1)
        plt.ylabel(None)
        plt.title(y)
        if self.output is not None:
            fig = ax.get_figure()
            fig.savefig(self.output + f"{y}.png")
