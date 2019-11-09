function plot_aerial(force, aerial_vals, aerial_loc, stance_begin, stance_end)
%PLOT_AERIAL Plots aerial phases and value at middle of each aerial phase. 
%   Visualizes the values used to account for the drift in [detrend.m]
%
%   INPUTS
%   ------
%   force: Nx1 array of force signal
%   aerial_vals: force signal from middle of each aerial phase.
%   aerial_loc: array of frame indexes for values in [aerial_vals] in trial.
%   stance_begin: array of frames where initial conact occurs.
%   stance_end: array of frames where toe-off occurs.
%
%   EXAMPLE from [sample.m]
%   -------                    
%   plot_aerial(GRF_filt(:,3), aerial_vals, aerial_loc, stance_begin, stance_end)
%
%   Author: Ryan Alcantara | ryan.alcantara@colorado.edu | github.com/alcantarar/dryft
%   License: MIT (c) 2019 Ryan Alcantara
%   Distributed as part of [dryft] | github.com/alcantarar/dryft

aerial_begin = stance_end(1:end-1);
aerial_end = stance_begin(2:end);

colors = winter(length(aerial_begin));

%plot all aerial phases
figure
p1 = subplot(2,1,1);
title('Aerial phases (black dot is middle)','fontsize',16)
xlabel('Frames')
ylabel('Force [N]')
hold on
for i = 1:length(aerial_begin)
    plot(force(aerial_begin(i):aerial_end(i)),'color',colors(i,:))
    plot(aerial_loc(i)-aerial_begin(i), aerial_vals(i), 'k.')
end
grid on
hold off

%plot means of aerial phases
subplot(2,1,2);
title('Force measured at middle of aerial phases','fontsize',16)
xlabel('Step #')
ylabel('Force [N]')
hold on
for i = 1:length(aerial_begin)
    plot(i,aerial_vals(i),'o','color',colors(i,:), 'MarkerFaceColor', colors(i,:))
end
grid on
hold off
ylim([min(aerial_vals)-abs(min(aerial_vals)*0.2), max(aerial_vals)+abs(max(aerial_vals)*0.2)])

end

