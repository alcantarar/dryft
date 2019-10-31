function [trim] = trim_aerial(force, step_begin, step_end)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
figure
hold on
plot(force(step_begin(1): step_end(2)), 'LineWidth',1.5)
start_a = find(force(step_begin(1):step_end(2)) == force(step_end(1)) == 1);
end_a = find(force(step_begin(1):step_end(2)) == force(step_begin(2)) == 1);

plot([start_a, start_a], [0,max(force(step_begin(1):step_end(2)))],'k', 'LineWidth',2)
plot([end_a, end_a], [0,max(force(step_begin(1):step_end(2)))],'k', 'LineWidth',2)
title({'select where to trim off beginning/end of aerial phase.';'stay between black lines'})

bad_points = 1;

while bad_points == 1;
    points = ginput(2);
    points = sortrows(points,1);
    if sum(points(:,1) < start_a) > 0 || sum(points(:,1) > end_a) > 0
        disp("Can't trim negative amount. Select 2 points within aerial phase")
    else
        trim = round((points(1,1) - start_a + end_a - points(2,1))/2)
        disp(['trimming ', num2str(trim), ' frames from start/end of aerial phase'])
        bad_points = 0;
        close
    end
end
    
    

end

