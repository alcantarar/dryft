#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
import pandas as pnd
#import copy
  # %%  
def readcheck_input(filename):
    force_imported = (pnd.read_csv(filename,delimiter = ',',header = None)).as_matrix()
    if force_imported.shape[1] == 3:
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
    compare = (force[:,2] > threshold).astype(int)

    events = np.diff(compare)
    step_begin = np.squeeze(np.asarray(np.nonzero(events == 1)).transpose())
    step_end = np.squeeze(np.asarray(np.nonzero(events == -1)).transpose())

    #if trial starts with end of step, ignore
    step_end = step_end[step_end > step_begin[0]]
    #trim end of step_begin to match step_end. 
    step_begin = step_begin[0:step_end.shape[0]]
    #check step length
    if step_begin.shape != step_end.shape: raise IndexError('Number of step beginnings and ends are not the same! Check step_ID function.')
    #initialize 
    step_len = np.full(step_begin.shape, np.nan) #step begin and end should be same length...
    step_begin_all = np.full(step_begin.shape, np.nan)
    step_end_all = np.full(step_end.shape, np.nan)
    
    good_step = 0

    #LEARN FROM THIS: (u/TheBlackCat13):
#    for i_step_end, i_step_begin in zip(step_end,step_begin):
#        if i_step_end - i_step_begin > min_step_length: #removes false positives by comparing min step_length
#            step_begin_all[good_step] = i_step_begin
#            step_end_all[good_step] = i_step_end
#            good_step = good_step + 1
            
    #or alternatively can be vectorizedsince step_begin and step_end are the same size now (see initialization)
    step_len = step_end - step_begin
    good_step = step_len > min_step_length
    step_begin_all = step_begin[good_step]
    step_end_all = step_end[good_step]
    
    #print sizes
#    step_end_all = (step_end_all[~np.isnan(step_end_all)]).astype(int) #not needed anymore
#    step_begin_all = (step_begin_all[~np.isnan(step_begin_all)]).astype(int)
    print('Number of step begin/end:',step_end_all.shape[0], step_begin_all.shape[0])
    
    return step_begin_all, step_end_all

# %%
def plot_separated_steps(force,begin,end):
    '''
    plots separated steps on top of each other. Requires an array of beginning/end of stance phase indexes and 3d (dim: Nx3) force data.
    '''
    plt.figure()
    plt.title('All separated steps')
    plt.grid()
    for i in range(end.shape[0]): plt.plot(force[begin[i]:end[i],2])
    
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
    fig, ax = plt.subplots()
    ax.plot(force[begin[0]:end[1],2])
    start_a = force[begin[0]:end[1],2] == force[end[0],2]
    end_a = force[begin[0]:end[1],2] == force[begin[1],2]
    ax.axvline(start_a.nonzero(),color = 'k')
    ax.axvline(end_a.nonzero(),color = 'k')
    ax.set_title('select how much to trim off beginning/end of aerial phase (between black lines)')
    
    import warnings
    warnings.filterwarnings('ignore','.*GUI is implemented.*')
    #user input from mouse click
    points = np.asarray(plt.ginput(2),dtype = int)
    plt.close(fig)
    
    if points[0,0] < start_a.nonzero()[0][0]: 
        raise IndexError("Can't trim negative amount. Select 2 points between start/end of aerial phase")
    elif points[1,0] > end_a.nonzero()[0][0]: 
        raise IndexError("Can't trim negative amount. Select 2 points between start/end of aerial phase")
    else:
        trim = (np.round((points[0,0]-start_a.nonzero()[0][0] + end_a.nonzero()[0][0]-points[1,0])/2)).astype(int)
        print('trimming ',trim,' frames from the start/end of aerial phase')
        
        return trim
# %%
def plot_aerial_phases(force, aerial_means, begin, end, trim, colormap = plt.cm.viridis):
    '''
    aerial_means is an array of mean values for every aerial phase. 
    
    '''
    if aerial_means.shape[0] == begin.shape[0] == end.shape[0]:
        colors = colormap(np.linspace(0,1,begin.shape[0]))     
        plt.fig, (untrimp, trimp, meanp) = plt.subplots(3,1,sharex = False, figsize = (15,10))
        
        #plot of untrimmed aerial phases
        untrimp.set_title('untrimmed aerial phases')
        untrimp.grid()
        for i in range(begin.shape[0]):
            untrimp.plot(force[begin[i]:end[i],2],color = colors[i])  
        #plot of trimmed aerial phases    
        trimp.set_title('trimmed aerial phases')
        trimp.grid()
        for i in range(begin.shape[0]):
            trimp.plot(force[begin[i]+trim:end[i]-trim,2],color = colors[i])
        #plot all the means of trimmed aerial phases
        meanp.set_title('mean of trimmed aerial phases')
        meanp.set_xlabel('steps')
        meanp.grid()
        for i in range(begin.shape[0]):
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
    print('Number of aerial begin/end:',aerial_begin_all.shape[0],aerial_end_all.shape[0]) #matching number of step beginnings/ends
    
    if plots != False:
        plot_separated_steps(force_f, step_begin_all, step_end_all)

    # %% trim filtering artefact and calculate mean of each aerial phase
    trim = trim_aerial_phases(force_f, step_begin_all, step_end_all)
    
    #calculate mean force during aerial phase (foot not on ground, should be zero)
    aerial_means = np.full([aerial_begin_all.shape[0],3], np.nan)
    for i in range(aerial_begin_all.shape[0]):
        aerial_means[i,0] = np.mean(force_f[aerial_begin_all[i]+trim:aerial_end_all[i]-trim,0])
        aerial_means[i,1] = np.mean(force_f[aerial_begin_all[i]+trim:aerial_end_all[i]-trim,1])
        aerial_means[i,2] = np.mean(force_f[aerial_begin_all[i]+trim:aerial_end_all[i]-trim,2])
    
    #plot aerial phases
    if plots != False:
        plot_aerial_phases(force_f, aerial_means, aerial_begin_all, aerial_end_all, trim)
    
    # %% Detrend signal    
    force_fd = np.zeros(force_f.shape)
    diff_vals = []

    for i in range(aerial_means.shape[0]-1):
        diff_temp = (aerial_means[i,2]+aerial_means[i+1,2])/2 #mean between two subsequent aerial phases
        diff_vals.append(diff_temp)
        force_fd[step_begin_all[i]:step_begin_all[i+1],:] = force_f[step_begin_all[i]:step_begin_all[i+1],:] - diff_temp
        
    if plots != False:            
        #plot raw vs detrended
        plt.figure(figsize = (20,10))
        plt.plot(np.linspace(0,force_f.shape[0]/Fs,force_f.shape[0]),force_f[:,2], alpha = 0.7) #converted to sec
        plt.plot(np.linspace(0,force_f.shape[0]/Fs,force_f.shape[0]),force_fd[:,2],'r', alpha = 0.7) #converted to sec
        plt.grid()
        plt.legend(['original signal','detrended signal'],fontsize =16)
        plt.xlabel('Seconds', fontsize = 16)
    
    #calculate mean aerial for detrend data
    aerial_means_d = np.zeros(aerial_means.shape[0])
    for i in range(aerial_begin_all.shape[0]):
        aerial_means_d[i] = np.mean(force_fd[aerial_begin_all[i]+trim:aerial_end_all[i]-trim,2]) #just vertical force
    aerial_means_d = aerial_means_d[aerial_means_d !=0.0]

    if plots != False:
        #plot detrend vs old mean aerial
        plt.figure(figsize = (20,5))
        plt.title('mean of aerial phases')
        plt.xlabel('steps',fontsize = 16)
        plt.grid()
        #np.ylim([-20,20])
        for i in range(aerial_means.shape[0]-1):
            plt.plot(i,aerial_means[i,2],'.', color = 'tab:blue', label = 'original signal')
            plt.plot(i,aerial_means_d[i],'.', color = 'tab:red', label = 'detrended signal')
            plt.legend(['original signal','detrended signal']) #don't want it in loop, but it needs it?

    return force_fd, aerial_means, aerial_means_d 

# %% 
#NEXT: force_fd has a weird blip at the end. not getting the number of steps totally right. 
#also make more subplots instead of separated plots. plots are all or nothing anywyas
