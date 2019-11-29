from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "dryft",
    version = "1.0.4",
    packages = find_packages(),
    install_requires = ['numpy','pandas>=0.24.0','matplotlib','scipy'],
    author = "Ryan Alcantara",
    description = "A package to process biomechanical running data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email = "ryan.alcantara@colorado.edu",
    license = "MIT",
    url = "http://github.com/alcantarar/dryft",   # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
)

# instructions for installing packages: https://packaging.python.org/tutorials/packaging-projects/