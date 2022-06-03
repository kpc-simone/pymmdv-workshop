from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
import pandas as pd

def plot_trajectory(ax,trdf_filepath,window,arena_dims=None):
    trdf = pd.read_csv(trdf_filepath)
    
    # calculate the sampling rate
    SR = 1 / trdf['time'].diff().mean()
    
    # get the data for the specified time window
    idx0 = int(window[0] * SR)
    idx1 = int(window[1] * SR)
    seg_df = trdf.iloc[idx0:idx1,:].reset_index(drop=True)
    
    # plot the trajectory over the time window
    ax.plot(seg_df['xpos'],seg_df['ypos'],color='dimgray')
    ax.plot(seg_df['xpos'].iloc[0],seg_df['ypos'].iloc[0],marker='o',color='k')
    
    if arena_dims:
        ax.set_xlim(0,arena_dims[0])
        ax.set_ylim(0,arena_dims[1])
        ax.set_xlabel('x-position, (mm)')
        ax.set_ylabel('y-position, (mm)')

if __name__ == '__main__':
    # looks nice for animal-3
    
    # specify inputs to function
    trdf_filepath = askopenfilename(
                        title='Select position tracking .csv file to visualize',
                        filetypes=[('CSV Files', '*.csv'), ('All Files', '*.*')]
                        )
    window = [360,420]
    arena_dims = [410,190]
    
    # create figure and visualize the data
    plt.style.use('../multipanel_style.mplstyle')
    fig,ax = plt.subplots(1,1)
    plot_trajectory(ax, trdf_filepath, window=window, arena_dims = arena_dims)
    plt.show()