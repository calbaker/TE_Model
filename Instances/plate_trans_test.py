# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import numpy as np
import matplotlib.pyplot as plt
import os, sys

cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import platewall 
reload(platewall)

plate = platewall.PlateWall()

plate.nodes = 4.
plate.T_h = 300.
plate.T_c = 300.

plate.set_h()
plate.solve_ss()
plate.time = np.arange(0, 2., plate.t_step) # total run time (s)

h_exh = 0.2
plate.init_arrays()
plate.setup_transient(h_exh)

plate.solve_standalone(700., 500.)

# Plot configuration
FONTSIZE = 20
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5

plt.close('all')

fig1 = plt.figure()
for i in range(plate.time.size):
    if i%2 == 0:
        plt.plot(plate.x*1000., plate.T[:,i])

plt.xlabel('X coordinate (mm)')
plt.ylabel('Temperature (K)')
plt.grid()

plt.show()

