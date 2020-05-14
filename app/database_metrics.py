from app.image_collection import ImageCollection
from app.image_metrics import ImageMetrics
from matplotlib import pyplot as plt
from scipy.spatial import ConvexHull
from scipy.spatial import Delaunay
import numpy as np
import seaborn as sns
from matplotlib import rc


def describe_figure(filename, title, xlabel, ylabel):
    def decorator(func):
        def wrapper(obj):
            func(obj)
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.tight_layout()
            plt.savefig(obj.output_dir + filename, bbox_inches='tight')
        return wrapper
    return decorator

class DatabaseMetrics:
    def __init__(self, directory: str, output_dir: str):

        self.it = ImageCollection(directory)
        self.output_dir = output_dir
        self.si = list()
        self.cf = list()
        sns.set(style="white")
        rc('font', **{'size': 36, 'family': 'serif', 'serif': ['Computer Modern']})
        rc('text', usetex=True)


    def plot_all(self):
        self.plot_si_cf_plane()
        self.plot_convex_hull()
        self.plot_delaunay()

    def calculate_si_cf(self):
        for image in self.it:
            im = ImageMetrics(image)
            si, cf = im.calculate_si_cf()
            self.si.append(si)
            self.cf.append(cf)

    @describe_figure("si_cf_plane.png", "SI x CF plane", "Spatial Information", "Colorfullness")
    def plot_si_cf_plane(self, filename: str = "si_cf.png"):
        if not len(self.cf) or not len(self.si):
            self.calculate_si_cf()
        plt.clf()
        sns.scatterplot(self.cf, self.si)

    @describe_figure("convex_hull.png", "Convex Hull", "Spatial Information", "Colorfullness")
    def plot_convex_hull(self):
        points = np.vstack((self.cf, self.si)).T
        hull = ConvexHull(points)
        plt.clf()
        plt.plot(points[:, 0], points[:, 1], 'o')
        for simplex in hull.simplices:
            plt.plot(points[simplex, 0], points[simplex, 1], 'k-')

    @describe_figure("delaunay.png", "Delaunay triangulation", "Spatial Information", "Colorfullness")
    def plot_delaunay(self):
        points = np.vstack((self.cf, self.si)).T
        tri = Delaunay(points)

        fig, ax = plt.subplots(1, 1)
        plt.tight_layout()
        ax.triplot(points[:, 0], points[:, 1], tri.simplices.copy(), lw=1)

        hull = ConvexHull(points)
        for simplex in hull.simplices:
            ax.plot(points[simplex, 0], points[simplex, 1], 'r-')

    def __str__(self):
        return f"SI: {self.si}, CF: {self.cf}"
