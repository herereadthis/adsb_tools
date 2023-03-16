# Documentation

## ChatGPT stuff

A ton of the stuff in this package was done via ChatGPT.

### But first, the original ChatGPT prompt:

> write and structure a pep-8 valid and pylint-valid package that can be uploaded to pypi. This package should be able to take a list of dictionaries, where each dictionary has a latitude and longitude. by providing predefined coordinates, the package should return the dictionary that is closest to the predefined coordinates using haversine formula to calculate distance

```shell
python3 -m venv env
source env/bin/activate

also,

```shell
# add packages to requirements.txt
pip3 freeze > requirements.txt
```

#### setup.py build

# test and package the module
python -m pip install wheel
python setup.py sdist bdist_wheel
```

This will create a dist directory with a .tar.gz file and a .whl file.

```shell
# upload to PyPi using twine
python -m pip install twine
twine upload dist/*
```

#### pyproject.toml build

```shell
python3 -m pip install --upgrade build
python3 -m pip install --upgrade twine
python3 -m build
twine upload dist/*
```


#### Post installation example usage

```python
from adsb_tools.distance.calculate import find_closest

coordinates = [
    {'latitude': 37.7749, 'longitude': -122.4194},
    {'latitude': 51.5074, 'longitude': -0.1278},
    {'latitude': 35.6895, 'longitude': 139.6917},
    {'latitude': -33.8651, 'longitude': 151.2094}
]

target_lat = 40.7128
target_lon = -74.0060

closest_dict = find_closest(coordinates, target_lat, target_lon)

print(f"The closest dictionary is: {closest_dict}")
```

### Testing this package:

> Suppose I am working python application called "foo" that uses a package called "bar" that installed via pip. this "bar" package is also mine. How can i test changes to "bar" from within my "foo" application, but without having to upload the updated "bar" to pypi? 

To test changes to the "bar" package from within your "foo" application without having to upload the updated "bar" package to PyPI, you can use a local development workflow. Here are the general steps:

1. Clone the "bar" package repository to your local machine.
1. Make the changes you want to test in the "bar" package code.
1. Build a new version of the "bar" package. You can do this by running `python setup.py sdist bdist_wheel` in the root directory of the "bar" package.
1. Install the new version of the "bar" package locally. You can do this by running `pip install /path/to/bar/dist/bar-x.y.z-py3-none-any.whl`, where `/path/to/bar` is the path to the root directory of the "bar" package and `x.y.z` is the version number of the new package.
1. Test the changes to the "bar" package in your "foo" application.

When you're done testing the changes to the "bar" package, you can either revert the changes or make any necessary modifications and repeat the process. This local development workflow allows you to test changes to the "bar" package without having to upload the updated package to PyPI.