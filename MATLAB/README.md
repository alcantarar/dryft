# `dryft` port for MATLAB
#### Created by [Ryan Alcantara](https://alcantarar.github.io)
While `dryft` is a python package, I've ported it to MATLAB because many biomechanical researchers only know how to use 
MATLAB :disappointed:. Here is a quick overview of how to use the `dryft` MATLAB code. Open an [issue](https://github.com/alcantarar/dryft/issues) 
if there are problems or better yet, contribute code via a [pull requests](https://github.com/alcantarar/dryft/pulls) 
to improve this MATLAB version! 

## Using the MATLAB version of `dryft`
#### Download functions
First, you need to clone/download the following files located in the MATLAB folder:
* `detrend.m`
* `mean_aerial_force.m`
* `plot_aerial.m`
* `sample.m`
* `split_steps.m`
* `trim_aerial.m`
* `drifting_forces.txt` (force data from [Fukuchi et al. (2017)](https://peerj.com/articles/3298/) that was modified to 
drift 100 N in a sine wave pattern)

#### Add functions to MATLAB path
Then, open up `sample.m` and make sure the other functions are located in your MATLAB path. If you're not sure how to do
this, consult the [MATLAB documentation](https://www.mathworks.com/help/matlab/ref/addpath.html). To test if the `dryft`
functions are in your path, run `help detrend` in the MATLAB command window. It should return the help page should if the 
function was successfully added to your MATLAB path. 

####  Using MATLAB version of `dryft`
The `sample.m` script serves as a tutorial, using the `drifting_forces.txt` as an example 3D ground reaction force trial.

## Licensing

This is distributed as part of `dryft`, which is licensed under the MIT License. 
Copyright 2019 [Ryan Alcantara](https://alcantarar.github.io).
