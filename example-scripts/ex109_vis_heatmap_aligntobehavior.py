# ex17_vis_pca_behavior.py
from tkinter.filedialog import askopenfilename
from sklearn.preprocessing import StandardScaler
from tkinter.filedialog import askopenfilename
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys,os

def show_heatmap_aligntobehavior(ax,sudf_filepath,behavior,display_padding_before,display_padding_after,cmap):

    sudf = pd.read_csv(sudf_filepath)
    SR = 1 / sudf['time'].diff().mean()
    # print(SR) # check calculated sample rate
    
    # load and transform behavioral data
    animal = os.path.basename(sudf_filepath).split('-')[0]  # get animal name for behavior file
    bhdf = pd.read_csv(os.path.join(os.path.dirname(__file__),'../example-data/{}-behavior.csv'.format(animal)))
    bhdf['behavior'] = bhdf['Behaviour']
    bhdf['bout start'] = bhdf[' start_time(ms)']
    bhdf['bout stop'] = bhdf['bout start'].shift(-1)
    bhdf['duration'] = bhdf['bout stop'] - bhdf['bout start']
    bhdf = bhdf.drop(bhdf[bhdf['behavior'] == 'VIDEO_END'].index)      # drop VIDEO_END
    bhdf = bhdf.drop(['Behaviour',' start_time(ms)'],axis=1).reset_index(drop=True)
    # print(sudf.shape, bhdf_dc.shape)      # check sizes of data frames
    
    bhdf = bhdf[bhdf['behavior'] == behavior].reset_index(drop=True)
    bhdf_sorted = bhdf.sort_values('duration')
    # print(bhdf_sorted.tail())
    longest_bout_row = bhdf_sorted.iloc[-1,:]
    # print(longest_bout_row['bout start'],longest_bout_row['bout stop'])
    
    # ignore 'time' in calcium
    sort_df = sudf.drop('time',axis=1).reset_index(drop=True)
    idx00 = int( (longest_bout_row['bout start'] - display_padding_before) * SR) 
    idx01 = int( longest_bout_row['bout start'] * SR) 
    
    idx10 = int( longest_bout_row['bout start'] * SR) 
    idx11 = int( (longest_bout_row['bout stop'] + display_padding_after) * SR) 
    
    delta_aucs = []
    # ignore 'time' column
    sort_df = sudf.drop('time',axis=1).reset_index(drop=True)
    for i,label in enumerate(sort_df.columns): 
        area_0 = sort_df.iloc[idx00:idx01,i].sum()
        area_1 = sort_df.iloc[idx10:idx11,i].sum()
        delta_aucs.append(area_1 - area_0)
    indxes = np.argsort( delta_aucs )[::-1]
    
    # focus on display interval and sort the cells
    disp0 = int( (longest_bout_row['bout start'] - display_padding_before) * SR )
    disp1 = int( (longest_bout_row['bout stop'] + display_padding_after) * SR )
    vis_df = sort_df.iloc[disp0:disp1,indxes].reset_index(drop=True)
    
    # normalize cell activity for visualization
    for col in vis_df.columns:
        vis_df[col] = ( vis_df[col] - vis_df[col].min() ) / ( vis_df[col].max() - vis_df[col].min() )

    ax.imshow(vis_df.transpose(),aspect='auto',interpolation='none',cmap=cmap)
    ax.axvline(int(display_padding_before*SR),linestyle='--',linewidth=1.0,color='white')
    ax.axvline(int( (longest_bout_row['duration']+display_padding_before)*SR),linestyle='--',linewidth=1.0,color='white')
    ax.set_xticks( [0,int(display_padding_before*SR),
                        int( (display_padding_before+longest_bout_row['duration'])*SR)] )
    ax.set_xticklabels( [ '{:.2f}'.format(t) for t in [-display_padding_before,0,longest_bout_row['duration']] ] )
    ax.set_xlabel('Time (s) from start of longest {} bout'.format(behavior))
    ax.set_ylabel(r'Cells $\to$')
    
# demo
if __name__ == '__main__':
    # looks nice with animal-2
    sudf_filepath = askopenfilename(
                        title='Select calcium traces .csv file to visualize neural activity/behavior relationship',
                        filetypes=[('CSV Files', '*.csv'), ('All Files', '*.*')]
        )
    behavior = 'groom'
    display_padding_before = 5
    display_padding_after = 5
    cmap = 'viridis'
    # notes
    
    plt.style.use('../multipanel_style.mplstyle')
    fig,ax = plt.subplots(1,1)
    show_heatmap_aligntobehavior(ax,sudf_filepath,behavior,display_padding_before,display_padding_after,cmap)
    plt.show()