function [good_aerial_begin, good_aerial_end] = find_good_aerial(stance_begin, stance_end, good_stances)
%FIND_GOOD_AERIAL Locates good aerial phases when bad stance phases are
%present.
%
%   INPUTS
%   ------
%   stance_begin: array of frames for initial contact. Output from
%       [split_steps.m].
%   stance_end: array of frames for toe-off. Output from [split_steps.m]
%   good_stances: logical array of which stance phase meets min/max_tc reqs
%
%   OUTPUT
%   ------
%   good_aerial_begin: frames of beginning of aerial phases not connected
%       to bad stance phases (per min/max_tc requirements)
%   aerial_loc: frames of end of aerial phases not connected
%       to bad stance phases (per min/max_tc requirements)
%
%   Author: Ryan Alcantara | ryan.alcantara@colorado.edu | github.com/alcantarar/dryft
%   License: MIT (c) 2019 Ryan Alcantara
%   Distributed as part of [dryft] | github.com/alcantarar/dryft

bs = find(good_stances == False);

end

