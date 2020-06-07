"""Metrics processing for single DB"""
import math
import os
from typing import Dict, List, Optional, Tuple

import numpy as np
import seaborn as sns
import yaml
from app.image_collection import ImageCollection, ImageIteratorInputError
from app.image_metrics import ImageMetrics
from matplotlib import pyplot as plt
from matplotlib import rc, rcParams
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.patches import Polygon
from scipy.spatial import ConvexHull, Delaunay

FIG_SIZE = (int(os.getenv("FIGURE_XSIZE", 6)), int(os.getenv("FIGURE_YSIZE", 6)))
XLIM = int(os.getenv("FIGURE_XLIM", 165))
YLIM = int(os.getenv("FIGURE_YLIM", 170))


class DatabaseMetricsError(Exception):
    """Generic database metrics error"""


def describe_figure(filename, xlabel: str, ylabel: str, title: str = None):
    """Handles common figure processiflang for different plots: labels, limits, titles, etc"""

    def decorator(func):
        def wrapper(obj):
            fig, ax = plt.subplots(figsize=FIG_SIZE)
            func(obj, ax)
            if obj.output_dir is not None:
                ax_title = title if title is not None else obj.label
                ax.set(
                    xlim=[0, XLIM],
                    ylim=[0, YLIM],
                    xlabel=xlabel,
                    ylabel=ylabel,
                    title=ax_title,
                )
                plt.tight_layout()
                plt.savefig(
                    f"{obj.output_dir}{obj.label}_{filename}", bbox_inches="tight"
                )
                plt.close()

        return wrapper

    return decorator


class DatabaseMetrics:
    """Class for calculating various metrics for single DB"""

    PRECISION = 40

    def __init__(
        self,
        directory: str,
        output_dir: Optional[str],
        max_si_cf: Tuple[float, float],
        label: str = "",
    ) -> None:
        """
        DatabaseMetrics constructor
        :param directory: path to the DB
        :param output_dir: directory in which output images should be saved
        :param max_si_cf: Maximum values of SI and CF across all analyzed databases
        :param label: DB label used in plot titles
        """
        try:
            self.it = ImageCollection(directory)
        except ImageIteratorInputError as err:
            raise DatabaseMetricsError(f"Error during creating ImageCollection '{err}'")
        self.directory = directory
        self.output_dir = output_dir
        self.label = label
        self.si: List[float] = list()
        self.cf: List[float] = list()
        self.norm_si: List[float] = list()
        self.norm_cf: List[float] = list()
        self.max_db_si, self.max_db_cf = max_si_cf
        self.points, self.norm_points = self.__calculate_si_cf()
        self.hull = ConvexHull(self.points)
        self.norm_hull = ConvexHull(self.norm_points)

        sns.set(style="white")
        rc("font", **{"size": 36, "family": "serif", "serif": ["Computer Modern"]})
        rc("text", usetex=True)

    def get_max_si_cf(self) -> Tuple[float, float]:
        """
        Returns maximum value of Spatial Information and Colorfulness for current DB
        :return: Tuple (max_si, max_cf)
        """
        max_si = np.amax(self.si)
        max_cf = np.amax(self.cf)
        return max_si, max_cf

    def get_si_cf_ranges(self) -> Tuple[float, float]:
        """
        Calculates SI and CF relative ranges
        :return: Tuple of (SI, CF) relative ranges
        """
        si_range = self.__get_range(self.si, self.max_db_si)
        cf_range = self.__get_range(self.cf, self.max_db_cf)
        return si_range, cf_range

    @staticmethod
    def __get_range(values: List[float], maximum: float) -> float:
        """
        Calculates relative ranges
        :param values: list of values to calculate relative ranges
        :param maximum: global maximum across multiple DBs
        :return: relative range
        """
        return (max(values) - min(values)) / maximum

    def get_coverage_area(self) -> float:
        """
        Calculates normalized convex hull area
        :return: Convex Hull area
        """
        return math.sqrt(self.norm_hull.volume)

    def plot_all(self) -> None:
        """
        Top-level method for generating all plots for the DB
        """
        self.__plot_si_cf_plane()
        self.__plot_convex_hull()
        self.__plot_fixed_radius()
        self.__plot_delaunay()

    def info(self) -> Dict[str, int]:
        try:
            with open(f"{self.directory}/.info.yaml", "r") as f:
                database_info = yaml.safe_load(f)
                return database_info["database"]
        except FileNotFoundError as err:
            raise DatabaseMetricsError(f"File not found: '{err}'")
        except yaml.YAMLError as err:
            raise DatabaseMetricsError(f"yaml could not be parsed: '{err}'")

    def __calculate_si_cf(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Creates list of SI and CF for each image in the DB
        """
        for image in self.it:
            im = ImageMetrics(image)
            si, cf = im.calculate_si_cf()
            self.si.append(si)
            self.cf.append(cf)
            self.norm_si.append(si / self.max_db_si)
            self.norm_cf.append(cf / self.max_db_cf)
        return (
            np.vstack((self.cf, self.si)).T,
            np.vstack((self.norm_cf, self.norm_si)).T,
        )

    @describe_figure("si_cf_plane.png", "Colorfulness", "Spatial Information")
    def __plot_si_cf_plane(self, ax=None) -> None:
        """Plots Spatial Information x Colorfulness plane"""
        sns.scatterplot(self.cf, self.si, ax=ax)

    @describe_figure("convex_hull.png", "Colorfulness", "Spatial Information")
    def __plot_convex_hull(self, ax=None) -> None:
        """Plots Convex Hull for SIxCF plane"""
        ax.plot(self.points[:, 0], self.points[:, 1], "o")
        for simplex in self.hull.simplices:
            ax.plot(self.points[simplex, 0], self.points[simplex, 1], "k-")

    @describe_figure("fixed_radius.png", "Colorfulness", "Spatial Information")
    def __plot_fixed_radius(self, ax=None, radius: float = 60) -> None:
        """Plots Convex Hull with fixed radius method for SIxCF plane"""
        radius *= 72.0 / plt.gcf().dpi
        ax.plot(self.points[:, 0], self.points[:, 1], "o", markersize=radius)
        ax.plot(self.points[:, 0], self.points[:, 1], "yx")
        for simplex in self.hull.simplices:
            ax.plot(self.points[simplex, 0], self.points[simplex, 1], "k-")

    def calculate_fill_rate_fixed_radius_area(self, radius: float = 60) -> float:
        """
        Calculates fill rate factor i.e. how well do images fill the convex hull using fixed radius approach
        This calculation is based on numerical approach, where ratio two areas is computed.
        One is area of circles inside convex hull and the other is convex hull area.
        Area of circles inside convex hull is computed as follows:
        One plot contains solid polygon representing convex hull and the other is reduced by points of given radius
        representing images in the database.
        The difference of these two plots is equivalent to points inside convex hull.

        :param radius: radius of the circle representing single image
        :return: fill rate factor [0-1]
        """
        context_usetex = rcParams["text.usetex"]
        rc("text", usetex=False)

        fig, ax = plt.subplots()
        plt.figure(figsize=(self.PRECISION, self.PRECISION))
        canvas = FigureCanvasAgg(fig)
        fig.patch.set_visible(False)

        radius *= 72.0 / fig.dpi
        p = Polygon(self.hull.points[self.hull.vertices], True, color="k")

        self.__plot_convex_hull_for_fill_rate(ax, p, radius, 10)
        array_with_points = self.__canvas_to_rgb(canvas)
        self.__plot_convex_hull_for_fill_rate(ax, p, radius, 0)
        array_without_points = self.__canvas_to_rgb(canvas)

        plt.close()

        diff = np.absolute(
            array_with_points.astype("float") - array_without_points.astype("float")
        ).astype("uint8")

        full = np.where(array_without_points > 128, 0, 1)
        diff = np.where(diff <= 128, 0, 1)
        rc("text", usetex=context_usetex)
        return min(np.sum(diff) / np.sum(full), 1.0)

    def __plot_convex_hull_for_fill_rate(self, ax, p, radius, zorder):
        ax.clear()
        ax.axis("off")
        ax.add_patch(p)
        ax.plot(
            self.points[:, 0], self.points[:, 1], "wo", markersize=radius, zorder=zorder
        )

    @staticmethod
    def __canvas_to_rgb(canvas):
        canvas.draw()
        array = np.array(canvas.renderer.buffer_rgba()).copy()
        return np.delete(array, 3, 2)  # Remove alpha channel

    @describe_figure("delaunay.png", "Colorfulness", "Spatial Information")
    def __plot_delaunay(self, ax=None) -> None:
        """Plots Delaunay triangulation for SIxCF plane"""
        for simplex in self.hull.simplices:
            ax.plot(self.points[simplex, 0], self.points[simplex, 1], "r-")

        tri = Delaunay(self.points)
        ax.triplot(self.points[:, 0], self.points[:, 1], tri.simplices.copy(), lw=1)

    def __str__(self) -> str:
        """Returns lists of SI and CF"""
        return f"SI: {self.si}, CF: {self.cf}"
