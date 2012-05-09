"""This script runs the model for designs available from
heat sink usa""" 

# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import numpy as np
import matplotlib.pyplot as plt
import os,sys
from scipy.optimize import fsolve, fmin

# User Defined Modules
cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import hx
reload(hx)

leg_area = (0.002)**2

area_ratio = 0.849
fill_fraction = 3.85e-2
leg_length = 4.00e-4
current = 13.2

hx0 = hx.HX()

hx0.width       = (20. - 0.640) * 2.54e-2
hx0.exh.height  = (2.5 - 0.375) * 2.54e-2
hx0.cool.height = 1.25 * 2.54e-2
hx0.length      = 20. * 2.54e-2

hx0.plate.thickness = 0.375 * 2.54e-2

hx0.te_pair.I = current
hx0.te_pair.length = leg_length

hx0.te_pair.Ntype.material = 'MgSi'
hx0.te_pair.Ptype.material = 'HMS'

hx0.te_pair.set_all_areas(leg_area, area_ratio, fill_fraction)

hx0.te_pair.method = 'numerical'
hx0.type = 'counter'

thickness = 0.080 * 2.54e-2
spacing = (0.400 - 0.080) * 2.54e-2

hx0.exh.enh = hx0.exh.enh_lib.IdealFin()
hx0.exh.enh.thickness = thickness
hx0.exh.enh.spacing = (0.200 - 0.080) * 2.54e-2
hx0.exh.enh.l = 3. / 8. * 2.54e-2

hx0.cool.enh = hx0.cool.enh_lib.IdealFin()
hx0.cool.enh.thickness = thickness
hx0.cool.enh.spacing = (0.400 - 0.080) * 2.54e-2 

# hx0.apar_list.append(['self','exh','enh','l'])
# hx0.apar_list.append(['self','length'])

hx0.exh.T_inlet = 800.
hx0.cool.T_inlet_set = 300.
hx0.cool.T_outlet = 307.7

hx0.set_mdot_charge()

hx0.solve_hx()

power0 = hx0.power_net

nodes_array = np.arange(20,212,1)
power = np.zeros(nodes_array.size) 

for i in range(nodes_array.size):
    print "\nSolving", i+1, "of", nodes_array.size 
    hx0.nodes = nodes_array[i]
    hx0.solve_hx()
    power[i] = hx0.power_net

    print hx0.power_net

power_norm = power / power0 
power_diff = (power - power0) / power0 * 100.

print "\nPreparing plots.\n"

# Plot configuration
FONTSIZE = 20
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5

plt.close()

plt.figure()
plt.plot(nodes_array, power_diff)

plt.xlabel('Number of Streamwise Nodes')
plt.ylabel('Change (%) in Power\nCompared to 25 Nodes')
plt.grid()
plt.subplots_adjust(bottom=0.12)
plt.subplots_adjust(left=0.20)

plt.savefig("../Plots/ad_hoc/streamwise.pdf")
plt.savefig("../Plots/ad_hoc/streamwise.png")

plt.show()

