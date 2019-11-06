function [aerial_means] = mean_aerial_force(force, step_begin, step_end, trim)
%MEAN_AERIAL_FORCE Calculates mean force signal during aerial phase of
%running.
%   INPUTS
%   ------
%   force: nx1 array of force signal to be detrended
%   step_begin: array of frames for initial contact. Output from
%       [split_steps.m].
%   step_end: array of frames for toe-off. Output from [split_steps.m]
%   trim: number of frames to trim from beginning/end of aerial phase.
%       Output from [trim_aerial.m].
%
%   OUTPUT
%   ------
%   aerial_means: mean force signal for all aerial phases in trial.
%
%   Author: Ryan Alcantara | ryan.alcantara@colorado.edu | github.com/alcantarar/dryft
%   License: MIT (c) 2019 Ryan Alcantara
%   Distributed as part of [dryft] | github.com/alcantarar/dryft

%define aerial phases
aerial_begin = step_end(1:end-1);
aerial_end = step_begin(2:end);
aerial_len = aerial_end - aerial_begin;

if aerial_len < trim*2
    error('Trim amount is greater than aerial phase length. If trim selection was reasonable, adjust threshold or min/max_step in split_step.m')
elseif size(force,2) > 1
    error('size(force,2) > 1. Must be nx1 array.')
end

for i = 1:length(aerial_begin)
    aerial_means(i) = mean(force(aerial_begin(i)+trim : aerial_end(i)-trim));
end



end

