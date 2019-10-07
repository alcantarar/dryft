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
    1); %(d)isplay plots = True

% Identify where aerial phase occurs (feet not on ground)                                
aerial_begin =  step_end(1:end-1);
aerial_end = step_begin(2:end);

                         