# `dryft` for MATLAB
#### Created by [Ryan Alcantara](https://alcantarar.github.io)
While `dryft` is a Python package, I made a MATLAB version because many biomechanical researchers only know how to use
MATLAB :disappointed:. Here is a quick overview of how to use the `dryft` MATLAB code. Open an [issue](https://github.com/alcantarar/dryft/issues) 
if there are problems or better yet, contribute code via a [pull requests](https://github.com/alcantarar/dryft/pulls) 
to improve this MATLAB version! 

## Using the MATLAB version of `dryft`
#### Download functions
First, you need to clone/download the following files located in the MATLAB folder:
* `aerial_force.m`
* `detrend.m`
* `find_good_aerial.m`
* `plot_aerial.m`
* `sample.m`
* `split_steps.m`
* `custom_drift_S001runT25.csv` (force data from [Fukuchi et al. (2017)](https://peerj.com/articles/3298/) that was
modified to have drift)

#### Add functions to MATLAB path
Open up `sample.m` and make sure the functions are located in your MATLAB path. If you're not sure how to do
this, consult the [MATLAB documentation](https://www.mathworks.com/help/matlab/ref/addpath.html). To confirm that the `dryft`
functions are in your path, run `help detrend` in the MATLAB command window. It should return the help page if the
function was successfully added to your MATLAB path. 

####  Using MATLAB version of `dryft`
The `sample.m` script serves as a tutorial, using the `custom_drift_S001runT25.csv` as an example vertical ground reaction force trial.

## Licensing

This is distributed as part of `dryft`, which is licensed under the MIT License. 
Copyright 2019 [Ryan Alcantara](https://alcantarar.github.io).
