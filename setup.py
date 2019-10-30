from setuptools import setup, find_packages

setup(
    name = "dryft",
    version = "1.0.1",
    packages = find_packages(),
    # metadata for upload to PyPI
    author = "Ryan Alcantara",
    description = "A package to process biomechanical running data",
    long_description = open('README.md').read(),
    author_email = "ryan.alcantara@colorado.edu",
    license = "MIT",
    url = "http://github.com/alcantarar/dryft",   # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
)