function plot_aerial(force, aerial_means, aerial_begin, aerial_end, trim)
%UNTITLED3 Summary of this function goes here
%   Detailed explanation goes here

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

