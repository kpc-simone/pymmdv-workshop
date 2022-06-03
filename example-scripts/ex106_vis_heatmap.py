# ex03_vis_heatmap.py
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def show_heatmap(ax,sudf_filepath,segment_0,segment_1,display_interval,cmap='inferno'):
    sudf = pd.read_csv(sudf_filepath)
    SR = 1 / sudf['time'].diff().mean()
    
    # calculate change in activity between segment 1 and segment 2 for each cell
    
    # get sample indexes for each segment start and end time
    idx00 = int( segment_0[0]*SR )
    idx01 = int( segment_0[1]*SR )
    idx10 = int( segment_1[0]*SR )
    idx11 = int( segment_1[1]*SR )

    delta_aucs = []
    
    # ignore 'time' column
    sort_df = sudf.drop('time',axis=1).reset_index(drop=True)
    for i,label in enumerate(sort_df.columns): 
        area_0 = sort_df.iloc[idx00:idx01,i].sum()
        area_1 = sort_df.iloc[idx10:idx11,i].sum()
        delta_aucs.append(area_1 - area_0)
    indxes = np.argsort( delta_aucs )[::-1]
    
    # focus on display interval and sort the cells
    disp0 = int( display_interval[0]*SR )
    disp1 = int( display_interval[1]*SR )
    vis_df = sort_df.iloc[disp0:disp1,indxes]
    
    # normalize cell activity for visualization
    for col in vis_df.columns:
        vis_df[col] = ( vis_df[col] - vis_df[col].min() ) / ( vis_df[col].max() - vis_df[col].min() )

    # generate the heatmap and add axis labels
    ax.imshow(vis_df.transpose(),aspect='auto',interpolation='none',cmap=cmap)
    seg_len = (segment_0[1]-segment_0[0])*SR
    ax.axvline( seg_len , color='white',linestyle='--',linewidth=1.0)
    xticks = [ k*seg_len for k in range(0,4) ]
    xticklabels = [ (t-seg_len)/SR for t in xticks ]
    ax.set_xticks( xticks )
    ax.set_xticklabels( xticklabels )
    ax.set_ylabel(r'Cells$\to$')
    ax.set_xlabel('Time (s) from onset of experimental condition')
        
if __name__ == '__main__':
    
    # specify inputs to function
    sudf_filepath = askopenfilename(
                        title='Select traces .csv file to visualize',
                        filetypes=[('CSV Files', '*.csv'), ('All Files', '*.*')]
                        )
    segment_0 = [240,300]
    segment_1 = [300,360]
    display_interval = [240,420]
    
    # create figure and visualize the data
    plt.style.use('../multipanel_style.mplstyle')
    fig,ax = plt.subplots(1,1)
    show_heatmap(ax,sudf_filepath,
                        segment_0 = segment_0,
                        segment_1 = segment_1,
                        display_interval = display_interval)
    plt.show()