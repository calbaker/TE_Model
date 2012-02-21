# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import numpy as np
import matplotlib.pyplot as plt
import os,sys
from scipy.optimize import fsolve
from mayavi import mlab

# User Defined Modules
cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
    
dirpath = '../data/TE_sensitivity/'
current_array = np.load(dirpath+'current_array.npy')
fill_array = np.load(dirpath+'fill_array.npy')
leg_height_array = np.load(dirpath+'leg_height_array.npy') * 1.e3

power_net_array = np.load(dirpath+'power_net_array.npy') 

VMIN = 0.9 * power_net_array.max()

mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(power_net_array),
                            plane_orientation='x_axes',
                            slice_index=current_array.size / 2,
                                 vmin=VMIN
                        )
mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(power_net_array),
                            plane_orientation='y_axes',
                            slice_index=fill_array.size / 2,
                                 vmin=VMIN
                        )
mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(power_net_array),
                            plane_orientation='z_axes',
                            slice_index=leg_height_array.size / 2,
                                 vmin=VMIN
                        )
mlab.colorbar(title='Power (kW)')
mlab.xlabel('Current (A)')
mlab.ylabel('Fill Fraction (A)')
mlab.zlabel('Leg Height (mm)')

mlab.outline()
