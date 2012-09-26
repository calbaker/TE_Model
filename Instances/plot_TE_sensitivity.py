# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import os
import sys

# User Defined Modules
cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
    
data_dir = '../output/te_design_space/'
current_array = np.load(data_dir + 'current_array.npy') 
fill_array = np.load(data_dir + 'fill_array.npy') * 100.
leg_height_array = np.load(data_dir + 'leg_height_array.npy') * 1.e3
power_I_fill = np.load(data_dir + 'power_I_fill')
power_fill_height = np.load(data_dir + 'power_fill_height')
power_height_I = np.load(data_dir + 'power_height_I')

# Plot configuration
FONTSIZE = 20
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5

plt.close()

fig = plt.figure()
ax = fig.gca(projection='3d')
X, Y, Z = current_array, fill_array, leg_height_array * 1e3

cset = ax.contourf(X, Y, Z, zdir='z', offset=-100)
cset = ax.contourf(X, Y, Z, zdir='x', offset=-40)
cset = ax.contourf(X, Y, Z, zdir='y', offset=40)

ax.set_xlabel('Current (A)')
# ax.set_xlim(-40, 40)
ax.set_ylabel('Fill Fraction')
# ax.set_ylim(-40, 40)
ax.set_zlabel('Leg Height (mm)')
# ax.set_zlim(-100, 100)

plt.show()


