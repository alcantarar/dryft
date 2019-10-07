% Read in data from force plate
GRF = csvread('../sample/drifting_forces.txt');

% Apply Butterworth filter
Fs = 600;
Fc = 60;
Fn = (Fs/2);
[b, a] = butter(2, Fc/Fn);

GRF_filt = filtfilt(b, a, GRF);


% Identify where stance phase occurs (foot on ground)
[step_begin,step_end] = split_steps(GRF_filt(:,3),... %vertical GRF
    110,... %threshold
    0.2,... %min_tc
    0.4,... %max_tc
    Fs,... %Sampling Frequency 
    0); %(d)isplay plots = False

% Identify where aerial phase occurs (feet not on ground)                                
aerial_begin =  step_end(1:end-1);
aerial_end = step_begin(2:end);

% Determine average force signal during aerial phase.
% Must trim beginning and end of aerial phase to get true aerial phase
% value. Filtering smooths out rapid transitions at start/end.
trim = trim_aerial(GRF_filt(:,3), step_begin, step_end);                         
aerial_means = mean_aerial_force(GRF_filt(:,3), step_begin, step_end, trim);
plot_aerial(GRF_filt(:,3), aerial_means, aerial_begin, aerial_end, trim)

% Detrend signal
[vGRF_detrend, aerial_means_detrend] = detrend(GRF_filt(:,3),... %nx1 force array
    Fs,... %force sampling frequency
    aerial_means,... %mean force during aerial phase
    step_begin,... %tc_begin
    step_end,... %tc_end
    trim,... %trim off beginning and end of aerial phase
    1); %(d)isplay plots = True

% I think this process can be repeated over and over. Should try. 