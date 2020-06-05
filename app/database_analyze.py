"""Tools for calculating metrics for multiple DBs"""
import logging
import os
from enum import Enum
from typing import Dict, Optional

import numpy as np
import pandas as pd
import seaborn as sns
from app.database_collection import DatabaseCollection
from app.database_metrics import DatabaseMetrics, DatabaseMetricsError
from matplotlib import pyplot as plt
from matplotlib import rc
from scipy.stats import entropy


class SingleMetrics(Enum):
    """
    Set of metrics in dataframe without SI/CF split
    """

    AREA = "Area"
    FILL_RATE = "Fill rate"
    DIST_IMG = "Distorted images"
    DIST_TYPES = "Distortion types"
    DIST_LVLS = "Distortion levels"
    APPLIED_DIST = "Applied distortions"
    YEAR = "Year"
    PALETTE = "Palette"


class DoubleMetrics(Enum):
    """
    Set of metrics in dataframe with SI/CF split
    """

    UNIFORMITY = "Uniformity"
    RELATIVE_RANGES = "Relative ranges"


class DatabaseAnalyzeError(Exception):
    """Generic DatabaseAnalyze Error"""


class DatabaseAnalyze:
    """
    Analyze set of databases
    """

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

        self.df_single = pd.DataFrame(
            columns=[v.value for v in SingleMetrics], index=self.dc.directories
        )

        self.df_double = pd.DataFrame(
            columns=[v.value for v in DoubleMetrics],
            index=[
                np.array(self.dc.directories * 2),
                np.array(["SI"] * len(self.dc) + ["CF"] * len(self.dc)),
            ],
        )
        self.__create_palette()
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

    def __create_palette(self):
        palette = sns.color_palette("deep", len(self.dc))
        for p, db in zip(palette, self.dc):
            self.df_single.at[db, SingleMetrics.PALETTE.value] = p

    def __parse_info(self) -> None:
        """
        Gets info from yaml file
        """
        for db in self.dc:
            try:
                info = self.db_metric[db].info()
                self.df_single.at[db, SingleMetrics.YEAR.value] = info["year"]
                self.df_single.at[db, SingleMetrics.DIST_IMG.value] = info[
                    "distorted_images"
                ]
                self.df_single.at[db, SingleMetrics.DIST_TYPES.value] = info[
                    "distortion_types"
                ]
                self.df_single.at[db, SingleMetrics.DIST_LVLS.value] = info[
                    "distortion_levels"
                ]
                self.df_single.at[db, SingleMetrics.APPLIED_DIST.value] = info[
                    "applied_distortion"
                ]

            except DatabaseMetricsError:
                continue
        for metric in (
            SingleMetrics.DIST_IMG.value,
            SingleMetrics.DIST_TYPES.value,
            SingleMetrics.DIST_LVLS.value,
            SingleMetrics.APPLIED_DIST.value,
        ):
            self.__single_bar(metric, False)

    def __relative_ranges(self) -> None:
        """
        Calculates relative ranges
        """
        for db in self.dc:
            si_rr, cf_rr = self.db_metric[db].get_si_cf_ranges()
            self.df_double.at[(db, "SI"), DoubleMetrics.RELATIVE_RANGES.value] = si_rr
            self.df_double.at[(db, "CF"), DoubleMetrics.RELATIVE_RANGES.value] = cf_rr
        self.__double_bar(DoubleMetrics.RELATIVE_RANGES.value)

    def __convex_hull_area(self) -> None:
        """
        Calculates convex hull area
        """
        for db in self.dc:
            area = self.db_metric[db].get_coverage_area()
            self.df_single.at[db, SingleMetrics.AREA.value] = area
        self.__single_bar(SingleMetrics.AREA.value)

    def __fill_rate_factor(self) -> None:
        """
        Calculates fill rate factor based on fixed radius approach
        """
        for db in self.dc:
            fill_rate = self.db_metric[db].calculate_fill_rate_fixed_radius_area()
            self.df_single.at[db, SingleMetrics.FILL_RATE.value] = fill_rate
        self.__single_bar(SingleMetrics.FILL_RATE.value)

    def __uniformity(self) -> None:
        """
        Calculates uniformity for databases
        """
        for db in self.dc:
            si_uni = entropy(self.db_metric[db].si, base=10)
            cf_uni = entropy(self.db_metric[db].cf, base=10)
            print(self.df_double)
            self.df_double.at[(db, "SI"), DoubleMetrics.UNIFORMITY.value] = si_uni
            self.df_double.at[(db, "CF"), DoubleMetrics.UNIFORMITY.value] = cf_uni
        self.__double_bar(DoubleMetrics.UNIFORMITY.value)

    def __single_bar(self, y, unit_scale: bool = True):
        """
        Plots bar for given metric
        :param y: metric
        """
        plt.clf()
        df = self.df_single.sort_values(by=y, ascending=False)
        ax = sns.barplot(
            x=df.index, y=y, data=df, palette=df[SingleMetrics.PALETTE.value]
        )
        if unit_scale:
            plt.ylim(0, 1)
        plt.ylabel(None)
        plt.title(y)
        if self.output is not None:
            fig = ax.get_figure()
            fig.savefig(self.output + f"{y}.png")

    def __double_bar(self, y):
        """
        Plots double bar for given metric with SI/CF split
        :param y: metric
        """
        plt.clf()
        plt.cla()
        df = self.df_double.sort_values(by=y, ascending=False).reset_index()
        df = df.rename(columns={"level_0": "DB", "level_1": "Metric"})
        ax = sns.barplot(x="DB", y=y, hue="Metric", data=df)
        plt.ylim(0, 1)
        plt.ylabel(None)
        plt.title(y)
        if self.output is not None:
            fig = ax.get_figure()
            fig.savefig(self.output + f"{y}.png")
