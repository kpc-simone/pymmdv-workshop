# ex04_vis_pca.py

from tkinter.filedialog import askopenfilename
from sklearn.preprocessing import StandardScaler
from tkinter.filedialog import askopenfilename
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pandas as pd
import sys,os

def plot_pca_segments(ax,sudf_filepath,windows,colors):
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
    
    # print(pcdf.shape)
    # print(pcdf.head())
    # print(pcdf.tail())
    
    for epoch,(window,color) in enumerate(zip(windows,colors)):
        idx0 = int(window[0]*SR)
        idx1 = int(window[1]*SR)
        
        ax.plot(pcdf['PC 1'].iloc[idx0:idx1],
                    pcdf['PC 2'].iloc[idx0:idx1],
                    color=color,
                    label='Epoch {}'.format(epoch+1)
                    )
    ax.set_xlabel('PC 1')
    ax.set_ylabel('PC 2')
    
    for spine in ['top','right']:
        ax.spines[spine].set_visible(False)
    
# demo
if __name__ == '__main__':
    sudf_filepath = askopenfilename(
                        title='Select calcium traces .csv file to visualize with PCA',
                        filetypes=[('CSV Files', '*.csv'), ('All Files', '*.*')]
        )
    windows = [(100,200),(300,400),(400,500)]
    colors = ['r','g','b']
    
    # notes
    # window is epoch start and end times
    # to select another color: https://matplotlib.org/2.0.1/api/colors_api.html
    
    plt.style.use('../multipanel_style.mplstyle')
    fig,ax = plt.subplots(1,1)
    plot_pca_segments(ax,sudf_filepath,windows,colors)
    plt.show()