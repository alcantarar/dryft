function [volts_data_array, fd, sum_force, colnames] = HighSpeedV2F_Table(volts_data)
%HighSpeedV2F converts raw voltage output from CU's High Speed Treadmill to
%Newtons. 
%
%   Calibration Matrix values pulled from "Export Forces and COP High
%   Speed Treadmill.v3s" V3D Pipeline. 
%
%   Parameters : 
%   ----------
%   volts_data :    N x 12 array of voltage data from treadmill
%   
%   Output :
%   ----------
%   {volts_data_array} :    nx12 matrix of volts data in {colnames} order
%   {fd} :                  nx12 matrix of newtons data in {colnames} order
%   {sum_force} :           nx3 matrix of summed forces (horiz,horiz,vert)
%   {colnames} :            order of transducer signals (Fx1, Fx2, etc.)
%
%   Error : 
%   ----------
%   Make sure input is just force data. Vicon sometimes stores marker
%   trajectories below the force data, but this needs to be removed. Just
%   export forces only. If unsure, scroll to bottom of force data in excel
%   (Ctrl + down-arrow will jump to next empty cell).
%
%   Author :    Ryan Alcantara | ryan.alcantara@colorado.edu |
%               github.com/alcantarar

%if you know what's good for you, don't change this calibration matrix.
calmat = [...
    -36.5075 0 0 0 0 0 0 0 0 0 0 0;...  %Fx1?
    0 -36.3925 0 0 0 0 0 0 0 0 0 0;...  %Fy1?
    0 0 142.454 0 0 0 0 0 0 0 0 0;...   %Fz1
    0 0 0 36.4102 0 0 0 0 0 0 0 0;...   
    0 0 0 0 36.2167 0 0 0 0 0 0 0;...
    0 0 0 0 0 143.057 0 0 0 0 0 0;...
    0 0 0 0 0 0 36.3198 0 0 0 0 0;...
    0 0 0 0 0 0 0 36.4503 0 0 0 0;...
    0 0 0 0 0 0 0 0 143.061 0 0 0;...
    0 0 0 0 0 0 0 0 0 -36.3428 0 0;...
    0 0 0 0 0 0 0 0 0 0 -36.4966 0;...
    0 0 0 0 0 0 0 0 0 0 0 143.414];
%sort table columns
ordered_cols = {'Fx1','Fy1','Fz1','Fx2','Fy2','Fz2','Fx3','Fy3','Fz3','Fx4','Fy4','Fz4'};
volts_data = volts_data(:,ordered_cols);
colnames = volts_data.Properties.VariableNames;
if sum(cellfun(@strcmp, volts_data.Properties.VariableNames,ordered_cols)) ~= 12
    error('table order column issue')
end
%convert to array because matlab tables suck
volts_data_array = table2array(volts_data);
%apply calibration matrix
if size(volts_data_array,2) == 12
    fd = volts_data_array(:,:)*calmat; %12 force channels (xyz*4t transducers)
    %swap X & Y
    force_data = NaN(length(volts_data_array),3); %initialize
    force_data(:,1) = fd(:,2) + fd(:,5) + fd(:,8) + fd(:,11);
    force_data(:,2) = fd(:,1) + fd(:,4) + fd(:,7) + fd(:,10);
    force_data(:,3) = fd(:,3) + fd(:,6) + fd(:,9) + fd(:,12);
    sum_force = force_data;
else
    error('volts_data not 12 channels')
end

