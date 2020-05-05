from app.image_collection import ImageCollection
from app.image_metrics import ImageMetrics
from matplotlib import pyplot as plt


class DatabaseMetrics:
    def __init__(self, directory: str, output_dir: str):
        self.it = ImageCollection(directory)
        self.output_dir = output_dir
        self.si = list()
        self.cf = list()

    def calculate_si_cf(self):
        for image in self.it:
            im = ImageMetrics(image)
            si, cf = im.calculate_si_cf()
            self.si.append(si)
            self.cf.append(cf)

    def si_cf_plane(self):
        plt.scatter(self.si, self.cf)
        plt.savefig(self.output_dir + "/si_cf.png")

    def __str__(self):
        return f"SI: {self.si}, CF: {self.cf}"