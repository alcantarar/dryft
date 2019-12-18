function [aerial, aerial_loc] = aerial_force(force, stance_begin, stance_end, good_stances)
%AERIAL_FORCE Calculates force signal at middle of aerial phase of running.
%   INPUTS
%   ------
%   force: nx1 array of force signal to be detrended
%   stance_begin: array of frames for initial contact. Output from
%       [split_steps.m].
%   stance_end: array of frames for toe-off. Output from [split_steps.m]
%   good_stances: logical array of which stance phases meet min/max_tc requirements   
%
%   OUTPUT
%   ------
%   aerial: force signal at middle of each aerial phases in trial.
%   aerial_loc: frame indexes for values in [aerial]
%
%   Author: Ryan Alcantara | ryan.alcantara@colorado.edu | github.com/alcantarar/dryft
%   License: MIT (c) 2019 Ryan Alcantara
%   Distributed as part of [dryft] | github.com/alcantarar/dryft

%define aerial phases
if any(good_stances == false)
    [aerial_begin, aerial_end] = dryft.find_good_aerial(stance_begin, stance_end, good_stances);
else
    aerial_begin = stance_end(1:end-1);
    aerial_end = stance_begin(2:end);
end

aerial_len = aerial_end - aerial_begin;
aerial_middle = round(aerial_len/2);

aerial = force(aerial_begin+aerial_middle);
aerial_loc = aerial_begin + aerial_middle;


end

