"""Metrics processing for single DB"""
from typing import List, Optional

import numpy as np
import seaborn as sns
from app.image_collection import ImageCollection, ImageIteratorInputError
from app.image_metrics import ImageMetrics
from matplotlib import pyplot as plt
from matplotlib import rc
from scipy.spatial import ConvexHull, Delaunay

FIG_SIZE = (6, 6)
XLIM = 165
YLIM = 170


class DatabaseMetricsError(Exception):
    """Generic database metrics error"""


def describe_figure(filename, xlabel: str, ylabel: str, title: str = None):
    """Handles common figure processiflang for different plots: labels, limits, titles, etc"""

    def decorator(func):
        def wrapper(obj):
            if obj.output_dir is not None:
                plt.figure(figsize=FIG_SIZE)
                func(obj)
                plt.title(title if title is not None else obj.label)
                plt.xlabel(xlabel)
                plt.ylabel(ylabel)
                plt.xlim(0, XLIM)
                plt.ylim(0, YLIM)
                plt.tight_layout()

                plt.savefig(
                    f"{obj.output_dir}{obj.label}_{filename}", bbox_inches="tight"
                )

        return wrapper

    return decorator


class DatabaseMetrics:
    """Class for calculating various metrics for single DB"""

    def __init__(self, directory: str, output_dir: str, label: str = "") -> None:
        """
        DatabaseMetrics constructor
        :param directory: path to the DB
        :param output_dir: directory in which output images should be saved
        :param label: DB label used in plot titles
        """
        try:
            self.it = ImageCollection(directory)
        except ImageIteratorInputError as err:
            raise DatabaseMetricsError(f"Error during creating ImageCollection '{err}'")
        self.output_dir = output_dir
        self.label = label
        self.si: List[float] = list()
        self.cf: List[float] = list()
        self.points: Optional[np.ndarray] = None
        self.__calculate_si_cf()
        print(self)
        sns.set(style="white")
        rc("font", **{"size": 36, "family": "serif", "serif": ["Computer Modern"]})
        rc("text", usetex=True)

    def plot_all(self) -> None:
        """
        Top-level method for generating all plots for the DB
        """
        self.__plot_si_cf_plane()
        self.__plot_convex_hull()
        self.__plot_delaunay()

    def __calculate_si_cf(self) -> None:
        """
        Creates list of SI and CF for each image in the DB
        """
        for image in self.it:
            im = ImageMetrics(image)
            si, cf = im.calculate_si_cf()
            self.si.append(si)
            self.cf.append(cf)
        self.points = np.vstack((self.cf, self.si)).T

    @describe_figure("si_cf_plane.png", "Colorfulness", "Spatial Information")
    def __plot_si_cf_plane(self) -> None:
        """Plots Spatial Information x Colorfulness plane"""
        sns.scatterplot(self.cf, self.si)

    @describe_figure("convex_hull.png", "Colorfulness", "Spatial Information")
    def __plot_convex_hull(self) -> None:
        """Plots Convex Hull for SIxCF plane"""
        hull = ConvexHull(self.points)
        plt.plot(self.points[:, 0], self.points[:, 1], "o")
        for simplex in hull.simplices:
            plt.plot(self.points[simplex, 0], self.points[simplex, 1], "k-")

    @describe_figure("delaunay.png", "Colorfulness", "Spatial Information")
    def __plot_delaunay(self) -> None:
        """Plots Delaunay triangulation for SIxCF plane"""
        hull = ConvexHull(self.points)
        for simplex in hull.simplices:
            plt.plot(self.points[simplex, 0], self.points[simplex, 1], "r-")

        tri = Delaunay(self.points)
        plt.triplot(self.points[:, 0], self.points[:, 1], tri.simplices.copy(), lw=1)

    def __str__(self) -> str:
        """Returns lists of SI and CF"""
        return f"SI: {self.si}, CF: {self.cf}"
