# distribution modules
import numpy as np
import matplotlib.pyplot as plt
import time, os, sys
from scipy.optimize import fmin

# local user modules
cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import te_pair
reload(te_pair)


length = 1.e-3
current = 3.5
area = (2.e-3)**2
area_ratio = 0.69 

te_pair = te_pair.TE_Pair()

te_pair.I = current
te_pair.Ptype.area = area
te_pair.length = length

te_pair.Ntype.material = 'MgSi'
te_pair.Ptype.material = 'HMS'

te_pair.Ptype.node = 0
te_pair.Ntype.node = 0
te_pair.T_c = 300.

te_pair.Ntype.area = te_pair.Ptype.area * area_ratio
te_pair.area_void = 0.
te_pair.method = 'numerical'
te_pair.set_constants()

current_array = np.linspace(0.5, 15, 16)
T_array = np.linspace(450, 800, 15)
power = np.zeros([current_array.size, T_array.size])

for i in range(current_array.size):
    te_pair.I = current_array[i]
    for j in range(T_array.size):
        te_pair.T_h_goal = T_array[j]
        te_pair.set_constants()
        te_pair.solve_te_pair()
        power[i,j] = te_pair.P 

# Plot configuration
FONTSIZE = 15
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 2.5
plt.rcParams['lines.markersize'] = 10
plt.rcParams['axes.formatter.limits'] = -3,3

plt.close('all')

plt.figure()
x_2d, y_2d = np.meshgrid(current_array, T_array)
TICKS = np.linspace(0, 800, 12)
LEVELS = np.linspace(0, 800, 12)
FCS = plt.contourf(x_2d, y_2d, power.T * 1.e6, levels=LEVELS) 
CB = plt.colorbar(FCS, orientation='vertical', format='%.0f', ticks=TICKS)
CB.set_label(r'Power ($\mu$W)')
plt.grid()
plt.xlabel('Current (A)')
plt.ylabel('Hot Side Temperature (K)')
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.15)
plt.subplots_adjust(right=0.7)

