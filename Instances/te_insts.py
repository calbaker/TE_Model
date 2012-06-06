# distribution modules
import matplotlib.pyplot as plt
import numpy as np
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

leg_area = (0.002) ** 2
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

te_pair.length = length
te_pair.leg_area_ratio = area_ratio
te_pair.fill_fraction = fill_fraction
#set leg length and such
te_pair.set_leg_areas()

te_pair.T_c_conv = 300.
te_pair.T_h_conv = 800.

U_hot = np.linspace(0.1, 2.5, 10)
U_cold = np.linspace(0.1, 2.5, 11)

P = np.zeros([U_hot.size, U_cold.size])

lengths = np.zeros([U_hot.size, U_cold.size])
fill_fractions = np.zeros([U_hot.size, U_cold.size])
currents = np.zeros([U_hot.size, U_cold.size])
area_ratios = np.zeros([U_hot.size, U_cold.size])

for i in range(U_hot.size):
    te_pair.U_hot = U_hot[i]

    print "\n\n\ncurrent =", te_pair.I

    for j in range(U_cold.size):

        print "\n\nsolving", i, ',', j, "of", U_hot.size, ',', U_cold.size

        te_pair.U_cold = U_cold[j]

        te_pair.optimize()

        lengths[i, j] = te_pair.length
        fill_fractions[i, j] = te_pair.fill_fraction
        currents[i, j] = te_pair.I
        area_ratios[i, j] = te_pair.leg_area_ratio

        P[i, j] = te_pair.P

save_dir = "../data/te_insts/"

np.save(save_dir + 'U_hot', U_hot)
np.save(save_dir + 'U_cold', U_cold)
np.save(save_dir + 'lengths', lengths)
np.save(save_dir + 'fill_fractions', fill_fractions)
np.save(save_dir + 'currents', currents)
np.save(save_dir + 'area_ratios', area_ratios)
np.save(save_dir + 'P', P)

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
