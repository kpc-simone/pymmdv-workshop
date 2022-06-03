# ex17_vis_pca_behavior.py
from tkinter.filedialog import askopenfilename
from sklearn.preprocessing import StandardScaler
from tkinter.filedialog import askopenfilename
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys,os

def decompress_annotation(SR,in_df,label_col_in,start_col_in,stop_col_in):
    index_col_out = 'time'
    label_col_out = label_col_in

    # create empty dataframe for out data
    out_df = pd.DataFrame( columns = [index_col_out,label_col_out] )
    idx0 = in_df[start_col_in].iloc[0]
    idxf = in_df[stop_col_in].iloc[-1]
    N = int((idxf - idx0) * SR)
    out_df[index_col_out] = np.linspace( idx0,idxf-1,N )

    # iterate through rows of in-data and add to out-data
    for index,row in in_df.iterrows():
        start = float(row[start_col_in])
        stop = float(row[stop_col_in])
        value = row[label_col_in]
        out_df.loc[(out_df[index_col_out] > start-1/SR) & (out_df[index_col_out] < stop+1/SR),label_col_out] = value

    # one-hot encode the out-data
    ohe_df = pd.get_dummies(out_df,prefix='',prefix_sep='')
    return ohe_df

def plot_pca_behavior(ax,sudf_filepath,behavior,color):

    sudf = pd.read_csv(sudf_filepath)
    SR = 1 / sudf['time'].diff().mean()
    # print(SR) # check calculated sample rate
    
    # ignore 'time' in calcium
    sudf.drop('time',axis=1).reset_index(drop=True)
    # print(sudf.head()) # check the data
    
    # normalize data (to a mean of zero and a standard deviation of one)
    X = StandardScaler().fit_transform(sudf.values)       # X: features to reduce dimensionality
    dimred_obj = PCA(n_components=2)
    principal_components = dimred_obj.fit_transform(X)
    pcdf = pd.DataFrame(data = principal_components, columns = ['PC 1', 'PC 2'])
    print('Explained variation per principal component: {}'.format(dimred_obj.explained_variance_ratio_))
    
    # load and transform behavioral data
    animal = os.path.basename(sudf_filepath).split('-')[0]  # get animal name for behavior file
    bhdf = pd.read_csv(os.path.join(os.path.dirname(__file__),'../example-data/{}-behavior.csv'.format(animal)))
    bhdf['behavior'] = bhdf['Behaviour']
    bhdf['bout start'] = bhdf[' start_time(ms)']
    bhdf['bout stop'] = bhdf['bout start'].shift(-1)
    bhdf = bhdf.drop(bhdf[bhdf['behavior'] == 'VIDEO_END'].index)      # drop VIDEO_END
    bhdf = bhdf.drop(['Behaviour',' start_time(ms)'],axis=1).reset_index(drop=True)
    
    # one-hot encoding of behavioral data
    bhdf_dc = decompress_annotation(SR=SR,
                                    in_df = bhdf,
                                    label_col_in = 'behavior',
                                    start_col_in = 'bout start',
                                    stop_col_in = 'bout stop',
                                    )
                                    
    # print(sudf.shape, bhdf_dc.shape)      # check sizes of data frames
    
    # visualize calcium data PCA colorized by behavior
    states = [0,1]
    colors = ['silver',color]
    for state, color in zip(states,colors):
        if state == 1:
            label_ = behavior
        else:
            label_ = 'not {}'.format(behavior)
            
        indices_to_show = bhdf_dc[behavior] == state
        ax.scatter(pcdf.loc[indices_to_show, 'PC 1'], 
                    pcdf.loc[indices_to_show, 'PC 2'], 
                    c = color, 
                    s = 5,
                    label = label_)
    
    ax.set_xlim(-5,10)
    ax.set_ylim(-10,10)
    ax.set_xlabel('PC 1')
    ax.set_ylabel('PC 2')
    ax.legend(loc = 'lower left')
    for spine in ['top','right']:
        ax.spines[spine].set_visible(False)
    
# demo
if __name__ == '__main__':
    sudf_filepath = askopenfilename(
                        title='Select calcium traces .csv file to visualize neural activity/behavior relationship',
                        filetypes=[('CSV Files', '*.csv'), ('All Files', '*.*')]
        )
    behavior = 'dig'
    color = 'saddlebrown'
    
    # notes
    # window is epoch start and end times
    # to select another color: https://matplotlib.org/2.0.1/api/colors_api.html
    
    plt.style.use('../multipanel_style.mplstyle')
    fig,ax = plt.subplots(1,1)
    plot_pca_behavior(ax,sudf_filepath,behavior,color)
    plt.show()