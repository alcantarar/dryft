function force_fd = detrend(force_f, aerial_vals, aerial_loc)
%DETREND Removes drift from running ground reaction force signal according
%to the aerial phase values.
%   INPUT
%   -----
%   force_f: nx1 array containing force signal to be detrended
%   aerial_vals: force signal at middle of aerial phase. Output from
%       [trim_aerial.m].
%   aerial_loc: array frame indexes where [aerial_vals] occur in [force_f]
%
%   OUTPUT
%   ------
%   force_fd: detrended force signal
%
%   Author: Ryan Alcantara | ryan.alcantara@colorado.edu
%   License: MIT (c) 2019 Ryan Alcantara
%   Distributed as part of [dryft] | github.com/alcantarar/dryft
%

% Fill nan array with aerial values according to where they are in force_f
drift = NaN(length(force_f),1);
drift(aerial_loc) = aerial_vals;
% Use cubic spline fill for nans, recreating the underlying drift in signal
try
    drift = fillmissing(drift, 'spline', 'EndValues','nearest'); %requires MATLAB 2016b or newer
catch
    drift = interp1(1:length(drift),drift,1:length(drift),'spline','extrap')';
end
% Subtract drift from force signal
force_fd = force_f-drift;

end

