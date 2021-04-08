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
%   Updated by Joshua Tacca 3/9/2021 to handle bad first/last stance phases
%   License: MIT (c) 2019 Ryan Alcantara
%   Distributed as part of [dryft] | github.com/alcantarar/dryft

   
bs = find(good_stances == false);
aerial_start = true(length(good_stances),1);
aerial_end = true(length(good_stances),1);

%if the first stance phase is bad, remove aerial phase afterwards:
if any(bs == 1) %first stance is bad
    x = find(bs == 1);
    %only need to get rid of aerial phase after first bad stance
    aerial_start(bs(x)) = false;
    aerial_end(bs(x)+1) = false;
    bs = bs(bs ~= 1);  % remove first bad stance since it's fixed now
end

%if the last stance phase is bad, remove aerial phase before: 
if any(bs == length(good_stances)) %last stance is bad
    y = find(bs == length(good_stances));
    %only need to get rid of aerial phase before bad stance
    aerial_start(bs(y)-1) = false;
    aerial_end(bs(y)) = false;
    bs = bs(bs ~= length(good_stances));  % remove last bad stance
end

% remove aerial phases for bad stances that are not the first/last ones:
aerial_end(bs) = false;
aerial_end(bs+1) = false;

aerial_start(bs) = false;
aerial_start(bs-1) = false;

% store good aerial phase info
good_aerial_begin = stance_end(aerial_start);
good_aerial_end = stance_begin(aerial_end);

good_aerial_begin = good_aerial_begin(1:end-1);
good_aerial_end = good_aerial_end(2:end);

end

