# Image database coverage

| Metric                     |                                                                                                                                                                                                                                          |
| :------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Continuous Integration** | [![CircleCI](https://circleci.com/gh/MatBucz/image-processing--database-coverage.svg?style=shield)](https://circleci.com/gh/MatBucz/image-processing--database-coverage)                                                                 |
| **Coverage**               | [![Coverage Status](https://coveralls.io/repos/github/MatBucz/image-processing--database-coverage/badge.svg?branch=master)](https://coveralls.io/github/MatBucz/image-processing--database-coverage?branch=master)                       |
| **Code Quality**           | [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/MatBucz/image-processing--database-coverage.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/MatBucz/image-processing--database-coverage/context:python)   |
|                            | [![Total alerts](https://img.shields.io/lgtm/alerts/g/MatBucz/image-processing--database-coverage.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/MatBucz/image-processing--database-coverage/alerts/)                          |
|                            | [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=MatBucz_image-processing--database-coverage&metric=alert_status)](https://sonarcloud.io/dashboard?id=MatBucz_image-processing--database-coverage)       |
| **Code Style**             | [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)                                                                                                                         |

This project provides set of tools allowing to analyze coverage of the image database.

It calculates set of metrics, which allow to compare how wide range of images the database covers.

Input images should be divided into several directories - i.e. images from each database
should have their own directory:

```
parent_dir
│
└───detabase 1
│   │   .info.yaml
│   │   image1.png
│   │   image2.png
│   │   ...
│
└───database 2
│   │   .info.yaml
│   │   imageA.png
│   │   imageB.png
│   │   ...
│
│   ...
│
└───database N
    │   .info.yaml
    │   imageX.png
    │   imageY.png
    │   imageZ.png
    │   ...
```

Moreover `.info.yaml` file might contain additional information about databases,
which will be plotted on separate figures. The structure of the yaml file is as follows:
```yaml
database:
  year: 2006
  distorted_images: 500
  distortion_types: 4
  distortion_levels: 6
  applied_distortion: 1
```

## Usage

Install requirements and run main.py:
```shell script
pip3 install -r requirements-dev.txt
python3 main.py
```

Or using docker environment:
```shell script
docker-compose up
```

## Test dataset
Test dataset is based on https://homepages.cae.wisc.edu/~ece533/images/

## Citation

If you use this tool please cite following paper:

M. Buczkowski, R. Stasiński,
_"Comparison of effective coverage calculation methods for image quality assessment databases",_
International Journal of Electronics and Telecommunications, 2018,
vol. 64, pp 307-313

Bibtex:
```
@article{buczkowski2018comparison,
  title={Comparison of effective coverage calculation methods for image quality assessment databases},
  author={Buczkowski, Mateusz and Stasi{\'n}ski, Ryszard},
  journal={International Journal of Electronics and Telecommunications},
  volume={64},
  number={3},
  pages={307--313},
  year={2018}
}
```

## Output

This tool saves results in separate figures, which can be montaged into following:

Exemplary convex hulls for databases:

![Convex hull](/output/convex_hull_montage.png "Convex hull")

Exemplary delaunay traingulations for databases:

![Delaunay traingulation](/output/delaunay_montage.png "Delaunay triangulation")

Exemplary number od distorted images

![Distorted_images](/output/bar_distorted_images.png "Distorted images")

Exemplary bar plot of relative ranges

![Relative_ranges](/output/bar_relative_ranges.png "Relative ranges")
