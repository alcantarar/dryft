function [trim] = trim_aerial(force, step_begin, step_end)
%TRIM_AERIAL Receives user input to determine how much it needs to trim off
%the beginning and end of aerial phase before calculating mean aerial force.
%   Trimming is required when detrending a force signal as filtering can
%   cause artificial negative values where zero values rapidly change to
%   positive values. These changes primarily occur during the beginning/end
%   of stance phase (and consequently the end/beginning of aerial phase). A
%   graph appears with vertical black lines at the beginning and end of an
%   aerial phase. Function is waiting for two mouse clicks on plot where
%   you'd like to trim the aerial phase. Click within the two black
%   vertical lines! Will apply mean of beginning/end trim to all steps.
%
%   INPUTS
%   ------
%   force: Nx1 array of force signal
%   step_begin: array of frames for initial contact. Output from
%       [split_steps.m].
%   step_end: array of frames for toe-off. Output from [split_steps.m]
%
%   OUTPUT
%   ------
%   trim: % number of frames to trim from beginning/end of aerial phase.
%
% Created by: Ryan Alcantara - ryan.alcantara@colorado.edu
%

figure
hold on
plot(force(step_begin(1): step_end(2)), 'LineWidth',1.5)
start_a = find(force(step_begin(1):step_end(2)) == force(step_end(1)) == 1);
end_a = find(force(step_begin(1):step_end(2)) == force(step_begin(2)) == 1);

plot([start_a, start_a], [0,max(force(step_begin(1):step_end(2)))],'k', 'LineWidth',2)
plot([end_a, end_a], [0,max(force(step_begin(1):step_end(2)))],'k', 'LineWidth',2)
title({'select where to trim off beginning/end of aerial phase.';'stay between black lines'})

bad_points = 1;

while bad_points == 1
    points = ginput(2);
    points = sortrows(points,1);
    if sum(points(:,1) < start_a) > 0 || sum(points(:,1) > end_a) > 0
        disp("Can't trim negative amount. Select 2 points within aerial phase")
    else
        trim = round((points(1,1) - start_a + end_a - points(2,1))/2);
        disp(['trimming ', num2str(trim), ' frames from start/end of aerial phase'])
        bad_points = 0;
        close
    end
end
    
    

end

