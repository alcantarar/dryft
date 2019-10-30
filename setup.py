# from distutils.core import setup
#
# setup(
#     name='dryft',
#     version='1.0',
#     packages=['dryft'],
#     license='MIT License',
#     long_description=open('README.md').read(),
#     description='Dryft package for running biomechanics data',
#     author='Ryan Alcantara',
#     author_email='ryan.alcantara@colorado.edu',
#     url='https://github.com/alcantarar/dryft',
# )


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dryft", # Replace with your own username
    version="1.0",
    author="Ryan Alcantara",
    author_email="ryan.alcantara@colorado.edu",
    description="A package for running biomechanics force data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alcantarar/dryft",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)