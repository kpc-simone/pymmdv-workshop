from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd
import numpy as np

def plot_trajectory_speedoverlay(ax,trdf_filepath,window,arena_dims,cmap='inferno'):
    trdf = pd.read_csv(trdf_filepath)
    
    # calculate the sampling rate
    SR = 1 / trdf['time'].diff().mean()
    
    # calculate speed
    b,a = signal.butter(10,0.1)
    trdf['xpos-filtered'] = signal.filtfilt(b,a,np.asarray(trdf['xpos']),padlen=2)
    trdf['ypos-filtered'] = signal.filtfilt(b,a,np.asarray(trdf['ypos']),padlen=2)
    trdf['xvel'] = trdf['xpos-filtered'].diff() * SR
    trdf['yvel'] = trdf['ypos-filtered'].diff() * SR
    trdf['speed'] = np.sqrt( trdf['yvel']**2 + trdf['xvel']**2 )
    
    # get the data for the specified time window
    idx0 = int(window[0] * SR)
    idx1 = int(window[1] * SR)
    seg_df = trdf.iloc[idx0:idx1,:].reset_index(drop=True)
    
    # plot the trajectory over the time window
    ax.plot(seg_df['xpos'],seg_df['ypos'],color='dimgray')
    ax.plot(seg_df['xpos'].iloc[0],seg_df['ypos'].iloc[0],marker='o',color='k')
    
    ax.scatter(seg_df['xpos'],seg_df['ypos'],c=seg_df['speed'],cmap=cmap,s=5,zorder=10)
    
    if arena_dims:
        ax.set_xlim(0,arena_dims[0])
        ax.set_ylim(0,arena_dims[1])

# demo
if __name__ == '__main__':
    # looks nice for animal-3
    
    # define input data and parameters for visualization
    trdf_filepath = askopenfilename(
                        title='Select position tracking .csv file to visualize',
                        filetypes=[('CSV Files', '*.csv'), ('All Files', '*.*')]
                        )
    window = [360,420]
    arena_dims = [410,190]

    plt.style.use('../multipanel_style.mplstyle')
    fig,ax = plt.subplots(1,1)
    plot_trajectory_speedoverlay(ax,
                        trdf_filepath,
                        window=window,
                        arena_dims = arena_dims,
                        cmap='inferno',
                        )
    plt.show()