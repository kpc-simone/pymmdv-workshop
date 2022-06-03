# ex13_vis_epoch_scatter.py
from tkinter.filedialog import askopenfilename
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import scipy.stats as stats
import pandas as pd
import numpy as np

def line(x,m,b):
    return m*x + b

def fit_line(ax,f1,f2,xlim,ylim):
    xs = np.array(f1).flatten()
    ys = np.array(f2).flatten()
    
    popt,pcov = curve_fit(line,xs,ys)
    fs = line(xs,*popt)
    rs = ys - fs
    ss_res = np.sum(rs**2)
    ss_tot = np.sum( ( ys - np.mean(ys) )**2 )
    rsq = 1 - ss_res / ss_tot
    rval = stats.pearsonr(fs,ys)[0]

    xmin = xlim[0]
    xmax = xlim[1]
    ymin = ylim[0]
    ymax = ylim[1]

    ts = np.linspace(xmin-0.1*(xmax-xmin),xmax+0.1*(xmax-xmin),len(xs))
    ax.plot(ts,line(ts,*popt),color='k')
    
    m,b = popt
    return rval,rsq,m,b

def plot_epoch_scatter(ax,sudf_filepath,baseline_epoch,comparison_epochs):
    sudf = pd.read_csv(sudf_filepath)
    SR = 1 / sudf['time'].diff().mean()
    # print(SR) # check calculated sample rate
   
    auc_df = sudf.drop('time',axis=1).reset_index(drop=True)    # ignore 'time' column
    
    # create an empty data structure (dictionary) to store the processed values
    delta_aucs = {}
    bsln_start = baseline_epoch[0]
    bsln_stop = baseline_epoch[1]
    # iterate over the comparison epochs
    for epoch_label,epoch_window in comparison_epochs.items():
        epoch_start,epoch_stop = epoch_window
        epoch_interval = epoch_stop - epoch_start
        
        idx00 = int( bsln_start * SR )
        idx01 = int( bsln_stop * SR )
        idx10 = int( epoch_start * SR )      # 
        idx11 = int( epoch_stop * SR )
        
        # iterate over each cell in the recording
        for i,label in enumerate(auc_df.columns): 
            auc_bl = auc_df.iloc[idx00:idx01,i].sum()
            auc_pk = auc_df.iloc[idx10:idx11,i].sum()
            
            # normalize the change by the length of the epoch interval
            delta_auc_norm = (auc_bl - auc_pk) / epoch_interval
            
            # append the value to the list for plotting
            if epoch_label not in delta_aucs:
                delta_aucs[epoch_label] = []
            
            delta_aucs[epoch_label].append( delta_auc_norm )
    
    # plot the data
    epoch_labels = list(comparison_epochs.keys())
    f1 = delta_aucs[ epoch_labels[0] ]
    f2 = delta_aucs[ epoch_labels[1] ]
    ax.scatter(f1,f2,color='k',s=2,zorder=10)

    # compute the axis limits
    xmin,xmax,ymin,ymax = min(f1),max(f1),min(f2),max(f2)
    min_ = min(xmin,ymin) - 0.1 * abs(min(xmin,ymin))
    max_ = max(xmax,ymax) + 0.1 * abs(max(xmax,ymax))
    ax.set_xlim(min_,max_)
    ax.set_ylim(min_,max_)

    # add some colors to identify cells that increase/decrease firing rate
    ax.axvspan(0.0,max_+0.1*(max_-min_),color='coral',alpha=0.6)
    ax.axhspan(0.0,max_+0.1*(max_-min_),color='powderblue',alpha=0.6)
    ax.axvspan(-0.05*(max_-min_),0.05*(max_-min_),color='silver',alpha=0.9)
    ax.axhspan(-0.05*(max_-min_),0.05*(max_-min_),color='silver',alpha=0.9)
    ax.axvline(0,linestyle=':',color='k')
    ax.axhline(0,linestyle=':',color='k')
    
    # fit a line and annotate fit parameters/goodness of fit
    rval,rsq,m,b = fit_line(ax,f1,f2,xlim=(min_,max_),ylim=(min_,max_))
    ax.text(0.95,0.2,'$r^2$ = {:4.3f}'.format(rsq),transform=ax.transAxes,ha='right',fontsize=8)
    ax.text(0.95,0.15,'$m$ = {:4.3f}'.format(m),transform=ax.transAxes,ha='right',fontsize=8)
    
    
    # add axis labels
    ax.set_xlabel(r'$\Delta$idF/F, {} - Baseline'.format(epoch_labels[0]))
    ax.set_ylabel(r'$\Delta$idF/F, {} - Baseline'.format(epoch_labels[1]))
    
if __name__ == '__main__':
    sudf_filepath = askopenfilename(
                        title='Select calcium traces .csv file to visualize relationship between cell activity between experiment epochs',
                        filetypes=[('CSV Files', '*.csv'), ('All Files', '*.*')]
                    )
    baseline_epoch = (60,240)
    comparison_epochs = {
        'Epoch1'   : (360,540),
        'Epoch2'   : (660,840),
    }
    
    plt.style.use('../multipanel_style.mplstyle')
    fig,ax = plt.subplots(1,1)
    plot_epoch_scatter(ax,sudf_filepath,baseline_epoch,comparison_epochs)
    plt.show()