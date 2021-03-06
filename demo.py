# pymmdv_demo.py

import matplotlib.pyplot as plt
import sys,os

# import source code from examples
sys.path.append(os.path.join(os.path.dirname(__file__),'example-scripts'))
from ex101_vis_trajectory import plot_trajectory
from ex102_vis_trajectory_speedoverlay import plot_trajectory_speedoverlay
from ex103_vis_running_bouts import plot_running_bouts

from ex105_vis_cell_traces import plot_cell_traces
from ex106_vis_heatmap import show_heatmap
from ex107_vis_epoch_scatter import plot_epoch_scatter

from ex108_vis_pca_segments import plot_pca_segments
from ex109_vis_heatmap_aligntobehavior import show_heatmap_aligntobehavior
from ex110_vis_pca_behavior import plot_pca_behavior

plt.style.use('multipanel_style.mplstyle')
fig,axes = plt.subplots(3,3,figsize=(10,8))

# trajectory w/ speed overlay
trdf_filepath = os.path.join(os.path.dirname(__file__),'example-data/animal3-position.csv')
plot_trajectory(axes[0,0],
                                trdf_filepath,
                                window=[360,420],
                                arena_dims = [410,190]
                                )

# trajectory w/ speed overlay
trdf_filepath = os.path.join(os.path.dirname(__file__),'example-data/animal3-position.csv')
plot_trajectory_speedoverlay(axes[0,1],
                                trdf_filepath,
                                window=[360,420],
                                arena_dims = [410,190],
                                cmap='inferno')

# running bouts, multiple animals
plot_running_bouts(axes[0,2],
                    trajectory_dir = '../example-data',
                    color='tab:cyan',
                    speed_thresh = 50.0,
                    min_bout_duration = 0.5,
                    )

# all cell traces in a recording sorted by time of peak within a given interval
sudf_filepath = os.path.join(os.path.dirname(__file__),'example-data/animal3-calcium.csv')
plot_cell_traces(axes[1,0],
                sudf_filepath,
                sort_interval = (210,218),
                key_times = (210,218,290,298,360,368,600,608,900,908),
                )

# heatmap of calcium traces from a single recording
sudf_filepath = os.path.join(os.path.dirname(__file__),'example-data/animal1-calcium.csv')
show_heatmap(axes[1,1],
                sudf_filepath,
                segment_0 = [240,300],
                segment_1 = [300,360],
                display_interval = [240,420],
                cmap='viridis'
                )

plot_epoch_scatter(axes[1,2],
                sudf_filepath,
                baseline_epoch = (60,240),
                comparison_epochs = {'Epoch1': (360,540),'Epoch2': (660,840)}
                )

# PCA of calcium traces for epochs in a single recording
sudf_filepath = os.path.join(os.path.dirname(__file__),'example-data/animal3-calcium.csv')
plot_pca_segments(axes[2,0],
                sudf_filepath,
                windows = [(100,200),(300,400),(400,500)],
                colors = ['r','g','b']
                )

# heatmap at onset of behavior bout
sudf_filepath = os.path.join(os.path.dirname(__file__),'example-data/animal2-calcium.csv')
show_heatmap_aligntobehavior(axes[2,1],
                    sudf_filepath,
                    behavior = 'groom',
                    display_padding_before = 5,
                    display_padding_after = 5,
                    cmap = 'viridis')

# PCA of calcium traces, points colorized by behavior
sudf_filepath = os.path.join(os.path.dirname(__file__),'example-data/animal2-calcium.csv')
plot_pca_behavior(axes[2,2],
                sudf_filepath,
                behavior = 'groom',
                color = 'darkorange'
                )

fig.tight_layout()
plt.show()