# distribution modules
import matplotlib.pyplot as plt
import time
import os
import sys

# local user modules
cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import te_pair
reload(te_pair)

t0 = time.clock()

leg_area = (0.002)**2
area_ratio = 0.849
fill_fraction = 3.85e-2
length = 4.00e-4
current = 13.2

te_pair = te_pair.TE_Pair()
# instantiate a te_pair object

te_pair.Ntype.material = 'MgSi'
te_pair.Ptype.material = 'HMS'
# declare materials to be used for property calculations

te_pair.I = current
# set current to be used in both legs

te_pair.set_all_areas(leg_area, area_ratio, fill_fraction)
# set all areas

te_pair.length = length
#set leg length

te_pair.set_constants()
# Sets a bunch of attributes that are usually held constant.

te_pair.T_c_conv = 300.
te_pair.T_h_conv = 800.

te_pair.U_cold = 2.
te_pair.U_hot = 0.5

te_pair.solve_te_pair()
te_pair.optimize()

# Plot configuration
FONTSIZE = 15
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 2.5
plt.rcParams['lines.markersize'] = 10
plt.rcParams['axes.formatter.limits'] = -3, 3

plt.close('all')
