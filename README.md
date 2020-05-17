# Image database coverage
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=MatBucz_image-processing--database-coverage&metric=alert_status)](https://sonarcloud.io/dashboard?id=MatBucz_image-processing--database-coverage)
[![CircleCI](https://circleci.com/gh/MatBucz/image-processing--database-coverage.svg?style=shield)](https://circleci.com/gh/MatBucz/image-processing--database-coverage)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This project provides set of tools allowing to analyze coverage of the image database.

It calculates set of metrics, which allow to compare how wide range of images the database covers.

Input images should be divided into several directories - i.e. images from each database
should have their own directory:

```
parent_dir
│
└───detabase 1
│   │   image1.png
│   │   image2.png
│   │   ...
│
└───database 2
│   │   imageA.png
│   │   imageB.png
│   │   ...
│
│   ...
│
└───database N
    │   imageX.png
    │   imageY.png
    │   imageZ.png
    │   ...
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

If you use this please cite following paper:

M. Buczkowski, R. Stasiński,
_"Comparison of effective coverage calculation methods for image quality assessment databases",_
International Journal of Electronics and Telecommunications, 2018,
vol. 64, pp 307-313

Bibtex:
```shell script
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
