# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from scipy.optimize import fsolve

# User Defined Modules
cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import te_pair
reload(te_pair)

leg_area = (0.002) ** 2.

area_ratio = 0.823
fill_fraction = 2.63e-2
leg_length = 3.55e-4
current = 12.5

te_design = te_pair.TE_Pair()
te_design.x0 = np.array([area_ratio, fill_fraction, leg_length,
                        current])

te_design.length = 48.e-2
te_design.width = 73.e-2
te_design.exh.height = 2.8e-2

te_design.te_pair.I = current
te_design.te_pair.length = leg_length

te_design.te_pair.Ntype.material = 'MgSi'
te_design.te_pair.Ptype.material = 'HMS'

te_design.te_pair.set_leg_areas()

te_design.te_pair.method = 'analytical'
te_design.type = 'counter'

te_design.exh.enh = te_design.exh.enh_lib.OffsetStripFin()

te_design.exh.T_inlet = 800.
te_design.cool.T_inlet_set = 300.
te_design.cool.T_outlet = 310.

te_design.set_mdot_charge()
te_design.cool.T_outlet = fsolve(te_design.get_T_inlet_error,
                                  x0=te_design.cool.T_outlet)

current_array = np.linspace(10, 14, 15)
fill_array = np.linspace(1.5, 3.5, 16) * 1.e-2
leg_height_array = np.linspace(0.1, 0.6, 17) * 1.e-3

power_net_array = np.zeros([current_array.size, fill_array.size,
                            leg_height_array.size])

for i in range(current_array.size):
    te_design.I = current_array[i]
    for j in range(fill_array.size):
        te_pair.fill_fraction = fill_array[j]
        te_design.set_leg_areas()
        for k in range(leg_height_array.size):
            te_design.te_pair.length = leg_height_array[k]
            te_design.solve_hx()

            power_net_array[i, j, k] = te_design.power_net

data_dir = '../output/TE_sensitivity/'
np.save(data_dir + 'power_net_array', power_net_array)
np.save(data_dir + 'current_array', current_array)
np.save(data_dir + 'fill_array', fill_array)
np.save(data_dir + 'leg_height_array', leg_height_array)

print "\nProgram finished."
print "\nPlotting..."

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
plt.plot(te_design.x * 100., te_design.exh.T_nodes, '-r', label='Exhaust')
plt.plot(
    te_design.x * 100., te_design.te_pair.T_h_nodes, '-g',
    label='TE_PAIR Hot Side'
    )
plt.plot(
    te_design.x * 100., te_design.te_pair.T_c_nodes, '-k',
    label='TE_PAIR Cold Side'
    )
plt.plot(te_design.x * 100., te_design.cool.T_nodes, '-b', label='Coolant')

plt.xlabel('Distance Along HX (cm)')
plt.ylabel('Temperature (K)')
#plt.title('Temperature v. Distance, '+te_design.type)
plt.grid()
plt.legend(loc='center left')
plt.subplots_adjust(bottom=0.15)

sys.execfile('plot_TE_sensitivity')
