import matplotlib.patches as patches
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd
import numpy as np
import sys,os

def get_bouts(df,col_name):    
    bouts_df = pd.DataFrame(columns = ['behavior','bout start','bout stop','bout duration'])
    in_a_bout = False
    for t,v in zip(df['time'],df[col_name]):
        if in_a_bout:
            if v == False:
                bout_stop = t
                in_a_bout = False
                bouts_df = bouts_df.append({
                    'behavior'      : col_name,
                    'bout start'    : bout_start,
                    'bout stop'     : bout_stop,
                    'bout duration' : bout_stop - bout_start,
                },ignore_index=True)
        else:
            if v == True:
                bout_start = t
                in_a_bout = True
                
    return bouts_df

def plot_bouts(ax,bouts_df,color,start_h=0,height=1.0):
    
    for index,bout in bouts_df.iterrows():
        start = bout['bout start']
        stop = bout['bout stop']
        dur = stop - start
        
        ax.add_patch(patches.Rectangle( 
                            (start,start_h),
                            dur,
                            height,
                            fill=True,
                            color = color,
                            alpha=1.0,
                           ))

def plot_running_bouts(ax,trajectory_dir,color,speed_thresh=10,min_bout_duration=1.0):

    # get all trajectory files
    trajectory_filenames = [f for f in os.listdir(os.path.join(os.path.dirname(__file__),trajectory_dir)) if 'position.csv' in f]
    animal_labels = []
    for t,trajectory_filename in enumerate(trajectory_filenames):
        trdf = pd.read_csv(os.path.join(os.path.dirname(__file__),trajectory_dir,trajectory_filename))
        animal_labels.append(trajectory_filename.split('-')[0])
        
        # derive speed of animal from instantaneous tail/snout positions
        # assuming positions of snout,tail are given in mm and sampling rate is 30 Hz
        SR = 1/ trdf['time'].diff().mean()
        # trdf['time'] = np.linspace(0,len(trdf)/SR,len(trdf))
        
        # calculate speed
        b,a = signal.butter(10,0.05)
        trdf['xpos-filtered'] = signal.filtfilt(b,a,np.asarray(trdf['xpos']),padlen=2)
        trdf['ypos-filtered'] = signal.filtfilt(b,a,np.asarray(trdf['ypos']),padlen=2)
        trdf['xvel'] = trdf['xpos-filtered'].diff() * SR
        trdf['yvel'] = trdf['ypos-filtered'].diff() * SR
        trdf['speed'] = np.sqrt( trdf['yvel']**2 + trdf['xvel']**2 )
        
        # stopping bouts are when the animal's speed falls below a user-specified level
        trdf['stop'] = trdf['speed'] > speed_thresh
        stdf = get_bouts(trdf,'stop')              # dataframe of stopping bout
        
        # freezing bouts are stopping bouts lasting longer than some user-specified duration
        rndf = stdf[stdf['bout duration'] > min_bout_duration]
        print('total time running for {} : {}'.format(animal_labels[-1],rndf['bout duration'].sum()))
    
        plot_bouts(ax,rndf,color,start_h = t)
        
    ax.set_yticks([int(n[-1])-0.5 for n in animal_labels])
    ax.set_yticklabels(animal_labels)
    ax.set_ylim(0,len(animal_labels))
    ax.set_xlim(0,trdf['time'].iloc[-1])
    ax.set_xlabel('Time (s)')

# demo
if __name__ == '__main__':

    # load the data
    trajectory_dir = '../example-data'
    color = 'tab:cyan'
    speed_thresh = 50.0            # assumes mm/s
    min_bout_duration = 0.5

    plt.style.use('../multipanel_style.mplstyle')
    fig,ax = plt.subplots(1,1)
    plot_running_bouts(ax,trajectory_dir,color,speed_thresh=speed_thresh,min_bout_duration=min_bout_duration)
    fig.tight_layout()
    plt.show()
