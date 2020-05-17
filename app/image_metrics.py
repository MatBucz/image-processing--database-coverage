"""Processing for single image in the DB"""
import logging
from typing import Tuple

import cv2
import numpy as np


class ImageMetricsInputError(Exception):
    """Image Metrics Error raised on wrong input params"""


class ImageMetrics:
    """Class for calculating metrics for single image in the database"""

    def __init__(self, img_filename: str) -> None:
        """
        Create ImageMetrics for specific image file
        :param img_filename: path and filename of the image file
        """
        logging.debug(f"Loading {img_filename}")
        if not isinstance(img_filename, str) or not len(img_filename):
            raise ImageMetricsInputError("Provide valid filename")
        self.img = cv2.imread(img_filename)
        if self.img is None:
            raise ImageMetricsInputError("Loaded image is None")

    def calculate_si_cf(self) -> Tuple[float, float]:
        """
        Calculates both Spatial Information and Colorfulnes for input image
        :return: tuple of SI and CF
        """
        si = self.__calculate_spatial_information()
        cf = self.__calculate_colorfulness()
        return si, cf

    def __calculate_spatial_information(self) -> float:
        """
        Calculates spatial information for input image
        :return: Spatial Information value
        """
        si_rgb = [0] * 3
        for d in range(self.img.shape[2]):
            sobelx = cv2.Sobel(self.img[:, :, d], cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(self.img[:, :, d], cv2.CV_64F, 0, 1, ksize=3)
            sobel = sobelx ** 2 + sobely ** 2
            si_rgb[d] = np.sqrt(self.img.shape[0] / 1080.0) * np.sqrt(
                np.sum(sobel) / (self.img.shape[0] * self.img.shape[1])
            )

        si = 0.299 * si_rgb[2] + 0.587 * si_rgb[1] + 0.114 * si_rgb[0]
        return si

    def __calculate_colorfulness(self) -> float:
        """
        Calculates Colorfulness for input image
        :return: Colorfulness value
        """
        rg = self.img[:, :, 2].astype("float") - self.img[:, :, 1].astype("float")
        yb = 0.5 * (
            self.img[:, :, 2].astype("float") + self.img[:, :, 1].astype("float")
        ) - self.img[:, :, 0].astype("float")

        sigma_rg = np.std(rg)
        sigma_yb = np.std(yb)

        mu_rg = np.mean(rg)
        mu_yb = np.mean(yb)
        cf = np.sqrt(sigma_rg ** 2 + sigma_yb ** 2) + 0.3 * np.sqrt(
            mu_rg ** 2 + mu_yb ** 2
        )
        return cf
