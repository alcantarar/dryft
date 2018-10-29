#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pylab as py
from scipy.signal import butter, filtfilt
#import copy
  # %%  
def readcheck_input(filename):
    force_imported = py.loadtxt(filename,delimiter = ',')
    if py.size(force_imported,1) == 3:
        return force_imported
    else: raise ValueError('force data must be Nx3 columns [horiz, horiz, vertical]')
   # %% 
def step_ID(force, threshold, min_step_length):
    '''
    This function reads in FILTERED *running* ground reaction force data and splits steps based on a force threshold.
    Author: Ryan Alcantara || ryan.alcantara@colorado.edu || github.com/alcantarar
    
    Parameters
    -------------
    force :             Nx3 array of FILTERED 3D [horizontal,horizontal,vertical] force data
    min_step_length :   Minimum number of frames the step ID algorithm will consider 1 step
    step_threshold :    Threshold in Newtons used to define heel-strike and toe-off. Please be responsible and set < 50N. 
    
    Returns
    -------------
    step_begin_all :    Array of frame indexes for beginning of stance phase
    step_end_all :      Array of frame indexes for end of stance phase
    (prints # of step beginnings/ends too)
    
    Example
    -------------
    >>> step_begin_all, step_end_all = step_ID(force_filtered,threshold = 20, min_step_length = 60) #20N threshold, 60 frame min length
    Number of step begin/end: 77 77
    array([101, 213, 323, 435]) #step_begin_all
    array([177, 289, 401, 511]) #step_end_all   
    
    
    '''
    #step Identification Forces over step_threshold register as step (foot on ground).
    compare = force[:,2] > threshold
    compare = compare.astype(int)
    events = py.diff(compare)
    step_begin = py.find(events == 1)
    step_end = py.find(events == -1)

    #if trial starts with end of step, ignore
    step_end = step_end[step_end > step_begin[0]]

    #check step length
    #initialize
    step_len = py.ndarray(py.size(step_end))
    step_begin_all = py.ndarray(py.size(step_begin))
    step_end_all = py.ndarray(py.size(step_end))
    step_len[:] = py.nan
    step_begin_all[:] = py.nan
    step_end_all[:] = py.nan
    
    good_step = 0
    
    for step_check in range(py.size(step_len)):
        step_len[step_check] = step_end[step_check] - step_begin[step_check]
        if step_end[step_check] - step_begin[step_check] > min_step_length: #removes false positives by comparing to min_step_length
            step_begin_all[good_step] = step_begin[step_check]
            step_end_all[good_step] = step_end[step_check]
            good_step = good_step+1                
    
    #remove unused NaN cells
    step_end_all = step_end_all[~py.isnan(step_end_all)]
    step_begin_all = step_begin_all[~py.isnan(step_begin_all)]
    #check sizes of begin/end
    step_end_all = step_end_all.astype(int)
    step_begin_all = step_begin_all.astype(int)
    print('Number of step begin/end:',py.size(step_end_all), py.size(step_begin_all))
    
    return step_begin_all, step_end_all

# %%
def plot_separated_steps(force,begin,end):
    '''
    plots separated steps on top of each other. Requires an array of beginning/end of stance phase indexes and 3d (dim: Nx3) force data.
    '''
    py.figure()
    py.title('All separated steps')
    py.grid()
    for i in range(py.size(end)): py.plot(force[begin[i]:end[i],2])
    
    # %%
def trim_aerial_phases(force, begin, end):
    '''
    Receives user input to determine how much it needs to trim off the beginning and end of the aerial phase. 
    This is done because filtering can cause artificial negative values where zero values rapidly change to positive values. 
    These changes primarly occur during the beginning/end of stance phase. 
    
    Graph should appear with vertical black lines at the beginning/end of the first aerial phase. Function is
    waiting for two mouse clicks where you'd like to trim the aerial phase. Click within the two black vertical lines!
    '''
    #plot a first 2 steps and get user input for how much to trim off beginning/end of aerial phase
    fig, ax = py.subplots()
    ax.plot(force[begin[0]:end[1],2])
    start_a = force[begin[0]:end[1],2] == force[end[0],2]
    end_a = force[begin[0]:end[1],2] == force[begin[1],2]
    ax.axvline(start_a.nonzero(),color = 'k')
    ax.axvline(end_a.nonzero(),color = 'k')
    ax.set_title('select how much to trim off beginning/end of aerial phase (between black lines)')
    
    import warnings
    warnings.filterwarnings('ignore','.*GUI is implemented.*')
    #user input from mouse click
    points = py.asarray(py.ginput(2),dtype = int)
    py.pause(.2)
    py.close(fig)
    
    if points[0,0] < start_a.nonzero()[0][0]: 
        raise IndexError("Can't trim negative amount. Select 2 points between start/end of aerial phase")
    elif points[1,0] > end_a.nonzero()[0][0]: 
        raise IndexError("Can't trim negative amount. Select 2 points between start/end of aerial phase")
    else:
        trim = round((points[0,0]-start_a.nonzero()[0][0] + end_a.nonzero()[0][0]-points[1,0])/2)
        trim = trim.astype(int)
        print('trimming ',trim,' frames from the start/end of aerial phase')
        
        return trim
    # %%
def plot_aerial_phases(force, aerial_means, begin, end, trim, colormap = py.cm.viridis):
    '''
    aerial_means is an array of mean values for every aerial phase. 
    
    '''
    if py.size(aerial_means,0) == py.size(begin,0) == py.size(end,0):
        colors = colormap(py.linspace(0,1,py.size(begin)))     
        py.fig, (untrimp, trimp, meanp) = py.subplots(3,1,sharex = False, figsize = (15,10))
        
        #plot of untrimmed aerial phases
        untrimp.set_title('untrimmed aerial phases')
        untrimp.grid()
        for i in range(py.size(begin)):
            untrimp.plot(force[begin[i]:end[i],2],color = colors[i])  
        #plot of trimmed aerial phases    
        trimp.set_title('trimmed aerial phases')
        trimp.grid()
        for i in range(py.size(begin)):
            trimp.plot(force[begin[i]+trim:end[i]-trim,2],color = colors[i])
        #plot all the means of trimmed aerial phases
        meanp.set_title('mean of trimmed aerial phases')
        meanp.set_xlabel('steps')
        meanp.grid()
        for i in range(py.size(begin)):
            meanp.plot(i,aerial_means[i,2],'o',color = colors[i])
            
    else: raise IndexError('aerial_means, begin, and end must be same length.')
# %%
def detrend_force(filename,Fs,Fc,min_step_length,step_threshold = 100,plots = False):
    '''
    This function reads in a comma separated file of *running* ground reaction force data and removes drift in a stepwise manner.
    Author: Ryan Alcantara || ryan.alcantara@colorado.edu || github.com/alcantarar
    
    Parameters
    -------------
    force_imported :    Nx3 array of 3D [horizontal,horizontal,vertical] force data in Newtons
    Fs :                Sampling frequency of force signal
    Fc :                Cut off frequency for 4th order zero-lag butterworth filter
    min_step_length :   Minimum number of frames the step ID algorithm will consider 1 step
    step_threshold :    (optional) threshold in Newtons used to define heel-strike and toe-off. default is 100N (better to be aggressive for detrending)
    plots :             (optional) T/F logical input to receive graphs depicting detrend process
    
    Returns
    -------------
    force_fd :          Nx3 array of detrended 3D force data 
    aerial_means :      Mean of force during aerial phase for original signal
    aerial_means_d :    Mean of force during aerial phase for detrended signal
    
    Raises
    -------------
    ValueError
        if imported file is not Nx3 dimensions. Requires 3D force data: [horizontal, horizontal, vertical].
    
    IndexError
        if number of aerial phase beginnings and aerial phase ends don't agree. check step_ID function.
        
    Examples
    -------------
    Explicitly defining parameters and output:
        
    >>> force_fd, aerial_means, aerial_means_d = detrend_force('drifting_forces.txt',Fs = 300, Fc = 60, min_step_length = 60, step_threshold = 100, plots = False)
    
    Without optional parameters and suppressing some outputs:
        
    >>> fname = '/Users/alcantarar/data/drifting_forces.csv'    
    >>> force_fd,_,_ = detrend_force(fname,300, 60, 60)

    '''
    
    force = readcheck_input(filename)
    #filter 4th order zero lag butterworth
    fn = (Fs/2)
    b,a = butter(2,Fc/fn)
    force_f = filtfilt(b,a,force,axis = 0) #filtfilt doubles order (2nd*2 = 4th order)
    
    # %% split steps and create aerial phases
    step_begin_all, step_end_all= step_ID(force_f,step_threshold, min_step_length)
    
    #create aerial phases (foot not on ground) and trim artefacts from filtering
    aerial_begin_all = step_end_all[:-1]
    aerial_end_all = step_begin_all[1:]
    print('Number of aerial begin/end:',py.size(aerial_begin_all),py.size(aerial_end_all)) #matching number of step beginnings/ends
    
    if plots != False:
        plot_separated_steps(force_f, step_begin_all, step_end_all)

    # %% trim filtering artefact and calculate mean of each aerial phase
    trim = trim_aerial_phases(force_f, step_begin_all, step_end_all)
    
    #calculate mean force during aerial phase (foot not on ground, should be zero)
    aerial_means = py.ndarray([py.size(aerial_begin_all),3])
    for i in range(py.size(aerial_begin_all)):
        aerial_means[i,0] = py.mean(force_f[aerial_begin_all[i]+trim:aerial_end_all[i]-trim,0])
        aerial_means[i,1] = py.mean(force_f[aerial_begin_all[i]+trim:aerial_end_all[i]-trim,1])
        aerial_means[i,2] = py.mean(force_f[aerial_begin_all[i]+trim:aerial_end_all[i]-trim,2])
    
    #plot aerial phases
    if plots != False:
        plot_aerial_phases(force_f, aerial_means, aerial_begin_all, aerial_end_all, trim)
    
    # %% Detrend signal    
    force_fd = py.zeros([py.size(force_f,0),3])
    diff_vals = []

    for i in range(py.size(aerial_means[:,2])-1):
        diff_temp = (aerial_means[i,2]+aerial_means[i+1,2])/2 #mean between two subsequent aerial phases
        diff_vals.append(diff_temp)
        force_fd[step_begin_all[i]:step_begin_all[i+1],:] = force_f[step_begin_all[i]:step_begin_all[i+1],:] - diff_temp
        
    if plots != False:            
        #plot raw vs detrended
        py.figure(figsize = (20,10))
        py.plot(py.linspace(0,py.size(force_f,0)/Fs,py.size(force_f,0)),force_f[:,2], alpha = 0.7) #converted to sec
        py.plot(py.linspace(0,py.size(force_f,0)/Fs,py.size(force_f,0)),force_fd[:,2],'r', alpha = 0.7) #converted to sec
        py.grid()
        py.legend(['original signal','detrended signal'],fontsize =16)
        py.xlabel('Seconds', fontsize = 16)
    
    
    #calculate mean aerial for detrend data
    aerial_means_d = py.zeros(py.size(aerial_means[:,2]))
    for i in range(py.size(aerial_begin_all)):
        aerial_means_d[i] = py.mean(force_fd[aerial_begin_all[i]+trim:aerial_end_all[i]-trim,2]) #just vertical force
    aerial_means_d = aerial_means_d[aerial_means_d !=0.0]

    if plots != False:
        #plot detrend vs old mean aerial
        py.figure(figsize = (20,5))
        py.title('mean of aerial phases')
        py.xlabel('steps',fontsize = 16)
        py.grid()
        #py.ylim([-20,20])
        for i in range(py.size(aerial_means,0)-1):
            py.plot(i,aerial_means[i,2],'.', color = 'tab:blue', label = 'original signal')
            py.plot(i,aerial_means_d[i],'.', color = 'tab:red', label = 'detrended signal')
            py.legend(['original signal','detrended signal']) #don't want it in loop, but it needs it?

    return force_fd, aerial_means, aerial_means_d 


# %%
 