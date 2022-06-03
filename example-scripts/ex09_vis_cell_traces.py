# ex03_vis_heatmap.py
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_cell_traces(ax,sudf_filepath,sort_interval,key_times):
    sudf = pd.read_csv(sudf_filepath)
    SR = 1 / sudf['time'].diff().mean()
    print(sudf.head())
    
    # get sample indexes for the sort interval
    idx0 = int( sort_interval[0]*SR )
    idx1 = int( sort_interval[1]*SR )
    
    # ignore 'time' column
    sort_df = sudf.drop('time',axis=1).reset_index(drop=True)
    
    # sort the cells by max time within a given interval
    max_times = []
    for i,label in enumerate(sort_df.columns): 
        max_time = sort_df[label].iloc[idx0:idx1].idxmax()
        max_times.append(max_time)
    indxes = np.argsort( max_times )[::-1]
    
    # focus on display interval and sort the cells
    vis_df = sort_df.iloc[:,indxes]
    
    # normalize cell activity for visualization
    for col in vis_df.columns:
        vis_df[col] = ( vis_df[col] - vis_df[col].min() ) / ( vis_df[col].max() - vis_df[col].min() )

    # plot the cells
    for i,cell_label in enumerate(list(vis_df)):
        ax.plot(sudf['time'],vis_df[cell_label]+(i),linewidth=0.5)

    # add the lines
    for key_time in key_times:
        ax.axvline(key_time,color='k',linestyle='--',linewidth=1.0)
        
    ax.set_yticks( [i for i in range(0,len(indxes))] )    
    ax.set_yticklabels( [i for i in indxes] )
    ax.set_ylabel(r'Cells $\to$')
    ax.set_xlabel('Time (s)')
    
if __name__ == '__main__':
    
    # specify inputs to function
    sudf_filepath = askopenfilename(
                        title='Select traces .csv file to visualize',
                        filetypes=[('CSV Files', '*.csv'), ('All Files', '*.*')]
                        )
    sort_interval = (210,218)
    key_times = (210,218,290,298,360,368,600,608,900,908)
    
    # create figure and visualize the data
    plt.style.use('../multipanel_style.mplstyle')
    fig,ax = plt.subplots(1,1,figsize=(8,3))
    plot_cell_traces(ax,sudf_filepath,
                        sort_interval = sort_interval,
                        key_times = key_times)
    plt.show()