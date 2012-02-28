# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import numpy as np
import matplotlib.pyplot as plt
import os,sys
from scipy.optimize import fsolve
from mayavi import mlab
from mayavi.api import Engine

# User Defined Modules
cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
    
dirpath = '../data/TE_sensitivity/'
current_array = np.load(dirpath+'current_array.npy') 
fill_array = np.load(dirpath+'fill_array.npy') * 100.
leg_height_array = np.load(dirpath+'leg_height_array.npy') * 1.e3

power_net_array = np.load(dirpath+'power_net_array.npy') 

VMIN = 0.9 * power_net_array.max()

mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(power_net_array),
                                 plane_orientation='x_axes',
                                 slice_index=np.unravel_index(power_net_array.argmax(),
                                                              power_net_array.shape)[0],
                                 vmin=VMIN
                        )
mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(power_net_array),
                                 plane_orientation='y_axes',
                                 slice_index=np.unravel_index(power_net_array.argmax(),
                                                              power_net_array.shape)[1],
                                 vmin=VMIN
                                 )
mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(power_net_array),
                                 plane_orientation='z_axes',
                                 slice_index=np.unravel_index(power_net_array.argmax(),
                                                              power_net_array.shape)[2],
                                 vmin=VMIN
                        )
axes = mlab.axes(ranges=[current_array.min(), current_array.max(),
                                 fill_array.min(), fill_array.max(),
                                 leg_height_array.min(),
                                 leg_height_array.max()]) 

mlab.colorbar(title='Power (kW)', nb_colors=12, orientation='vertical')
mlab.xlabel('Current (A)')
mlab.ylabel('Fill Fraction (%)')
mlab.zlabel('Leg Height (mm)')

mlab.outline()

