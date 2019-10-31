function plot_aerial(force, aerial_means, aerial_begin, aerial_end, trim)
%PLOT_AERIAL Plots untrimmed aerial phases, trimmed aerial phases, and the
%means of the trimmed aerial phases. 
%   Visualizes the means used to account for the drift in [detrend.m]
%
%   INPUTS
%   ------
%   force: Nx1 array of force signal
%   aerial_means: mean force signal for aerial phase. Output from
%       [trim_aerial.m].
%   aerial_begin: array of frames where aerial phase begins. see EXAMPLE.
%   aerial_end: array of frames where aerial phase ends. see EXAMPLE.
%   trim: number of frames to trim from beginning/end of aerial phase.
%       Output from [trim_aerial.m].
%
%   EXAMPLE from [sample.m]
%   -------
%   aerial_begin =  step_end(1:end-1);
%   aerial_end = step_begin(2:end);
%   trim = trim_aerial(GRF_filt(:,3), step_begin, step_end);                         
%   aerial_means = mean_aerial_force(GRF_filt(:,3), step_begin, step_end, trim);
%
%   plot_aerial(GRF_filt(:,3), aerial_means, aerial_begin, aerial_end, trim)
%
% Created by: Ryan Alcantara - ryan.alcantara@colorado.edu
%
colors = parula(length(aerial_begin));
%plot all untrimmed aerial phases
figure
p1 = subplot(3,1,1);
title('untrimmed aerial phases','fontsize',16)
xlabel('frames')
hold on
for i = 1:length(aerial_begin)
    plot(force(aerial_begin(i):aerial_end(i)),'color',colors(i,:))
end
grid on
hold off

%plot trimmed aerial phases
p2 = subplot(3,1,2);
title('trimmed aerial phases','fontsize',16)
xlabel('frames')
hold on
for i = 1:length(aerial_begin)
    plot(force(aerial_begin(i)+trim:aerial_end(i)-trim),'color',colors(i,:))
end
grid on
hold off

%plot means of trimmed aerial phases
subplot(3,1,3);
title('mean of trimmed aerial phases','fontsize',16)
xlabel('steps')
hold on
for i = 1:length(aerial_begin)
    plot(i,aerial_means(i),'o','color',colors(i,:), 'MarkerFaceColor', colors(i,:))
end
grid on
hold off
ylim([min(aerial_means)-abs(min(aerial_means)*0.2), max(aerial_means)+abs(max(aerial_means)*0.2)])

linkaxes([p1,p2],'y')

end

