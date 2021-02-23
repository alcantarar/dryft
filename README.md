# `dryft`
![visitors](https://visitor-badge.laobi.icu/badge?page_id=alcantarar.dryft)    
Read the published manuscript in the Journal of Open Source Software:    
[![DOI](https://joss.theoj.org/papers/10.21105/joss.01910/status.svg)](https://doi.org/10.21105/joss.01910)    

`dryft` is an open-source Python package that corrects running ground reaction force (GRF) 
signal drift. This package was developed for biomechanical researchers using force plates
or a force-measuring treadmill to collect an individual's GRF during running, but should work for split-belt treadmill
walking as well. Due to the prevalence of MATLAB in the field of Biomechanics, I have also developed a [set of
MATLAB functions](MATLAB) that operate like the Python package. However, this readme will 
focus on the use of the Python package.

## Table of Contents
* [Dependencies](#dependencies)
* [Recommended Installation](#recommended-installation)
* [How `dryft` Works](#how-dryft-works)
* [Using `dryft`](#using-dryft)
* [Contributing](#contributing)
* [Licensing](#licensing)

## Dependencies
This package was designed to work with and was tested with Python 3.6.7. 
Other python 3.X versions may be supported, provided dependency compatibilities and requirements are met.

The package requires the following dependencies: 
* numpy
* pandas *(0.24.0 or newer)*
* matplotlib
* scipy

## Installation
### Using virtualenv
On Windows:
```
git clone https://github.com/alcantarar/dryft.git
pip install virtualenv
python -m venv dryft-env
.\dryft-env\Scripts\activate
cd dryft
python setup.py install
```
On macOS or Linux:
```
git clone https://github.com/alcantarar/dryft.git
pip install virtualenv
python -m venv dryft-env
source dryft-env/bin/activate
cd dryft
python setup.py install
```
### Using pip:
```
git clone https://github.com/alcantarar/dryft.git
cd dryft
pip install -r requirements.txt
```
### Using Anaconda
You can use [Anaconda](https://www.anaconda.com/distribution/#download-section) to setup a Python 3.6.7 
environment to use this package. If you wish to setup a new environment, an Anaconda [environment](environment.yml) 
file is included to automatically install most dependencies. 
You can create/activate an anaconda environment and download dependencies using the Anaconda Prompt: 
```
git clone https://github.com/alcantarar/dryft.git
cd dryft
conda env create -f path\to\environment.yml
conda activate dryft-env
python setup.py install
```

## How `dryft` Works
<p align="center">
<img src="https://raw.githubusercontent.com/alcantarar/dryft/master/documentation/JOSS_submission/example_JOSS.png" width="700">
</p>  
Running is generally characterized by two phases: a stance and aerial phase. Only one foot is on the ground at a time during 
stance phase and both feet are off the ground during aerial phase. The force exerted by the body on the ground during 
aerial phase is zero and during stance phase it is greater than zero. If drift is present in the force signal, values 
during the aerial phase will no longer be zero. First, `dryft` calculates the force occurring during each aerial phase of
a continuous running trial. Then these aerial phase values are interpolated to the length of the trial using a 3rd order
spline fill. Lastly, the interpolated values, which represents the signal drift over time, are subtracted from the original 
trial. This effectively corrects for signal drift.

Another method of correcting drift is described by [Paolini *et al.* (2007)](https://www.ncbi.nlm.nih.gov/pubmed/16759895), 
where the mean force measured during the aerial phase is subtracted from the following stance phase. The success of this 
approach is highly dependent upon the method of identifying aerial phases in the vertical ground reaction force signal. If a 
force threshold is used to define the boundaries of each aerial phase, parts of the neighboring stance phases may 
be included in the calculation of the mean (left panel in the figure above). Additionally, this approach assumes no change in drift over the duration of a 
stance phase. The `dryft` package uses the force measured at the middle of each aerial phase
and spline interpolates between them to correct signal drift. This approach differs from the method described by Paolini 
*et al.* (2007) and currently available drift correction methods which can only account for 
[linear drift](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.detrend.html) or a constant 
[offset](https://www.c-motion.com/v3dwiki/index.php/FP_ZERO) 

## Using `dryft`

### Testing
Running the following from the command line will automatically test the installation of `dryft`:
```
python -m dryft.sample.test
```

### Tutorial
A notebook of `dryft.sample.test` is available [here](https://alcantarar.github.io/dryft/test.html) as a tutorial.

### Documentation
Please refer to the [documentation page](https://alcantarar.github.io/dryft/index.html)

## Contributing
To report an problem with `dryft`, please create a new [issue](https://github.com/alcantarar/dryft/issues).

Contact [alcantarar](https://github.com/alcantarar) with any support or general questions about `dryft`. I also welcome
meaningful contributions via [pull requests](https://github.com/alcantarar/dryft/pulls).

## Licensing

This package is licensed under the MIT License. Copyright 2019 [Ryan Alcantara](https://alcantarar.github.io).
