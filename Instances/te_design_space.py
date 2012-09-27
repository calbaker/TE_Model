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

area = (0.002) ** 2.
leg_area_ratio = 0.823
fill_fraction = 2.63e-2
length = 3.55e-4
current = 12.5

te_design = te_pair.TE_Pair()
te_design.Ptype.area = area
te_design.leg_area_ratio = leg_area_ratio
te_design.fill_fraction = fill_fraction
te_design.length = length
te_design.I = current

te_design.Ntype.material = 'MgSi'
te_design.Ptype.material = 'HMS'

te_design.set_leg_areas()

te_design.T_c_conv = 300.  # cold side convection temperature (K)
te_design.T_h_conv = 800.  # hot side convection temperature (K)

te_design.U_cold = 2.
# cold side overall heat transfer coeffcient (kW / (m ** 2 * K))
te_design.U_hot = 1.
# hot side overall heat transfer coeffcient (kW / (m ** 2 * K))

te_design.optimize()

current_array = np.linspace(0.5, 1.5, 10) * te_design.I
fill_array = (
    np.linspace(0.5, 1.5, current_array.size + 1) *
    te_design.fill_fraction * 1.e-2
    )
length_array = (
    np.linspace(0.5, 1.5, fill_array.size + 1) * te_design.length *
    1.e-3
    )

power_I_fill = np.zeros(
    [current_array.size, fill_array.size]
    )
power_fill_height = np.zeros(
    [fill_array.size, length_array.size]
    )
power_height_I = np.zeros(
    [length_array.size, current_array.size]
    )

for i in range(current_array.size):
    te_design.I = current_array[i]
    print "i =", i
    for j in range(fill_array.size):
        te_design.fill_fraction = fill_array[j]
        te_design.set_leg_areas()
        te_design.solve_te_pair()
        power_I_fill[i, j] = te_design.P_flux

te_design.I = current
te_design.fill_fraction = fill_fraction

for j in range(fill_array.size):
    te_design.fill_fraction = fill_array[j]
    te_design.set_leg_areas()
    print "j =", j
    for k in range(length_array.size):
        te_design.length = length_array[k]
        te_design.solve_te_pair()
        power_fill_height[j, k] = te_design.P_flux

te_design.fill_fraction = fill_fraction
te_design.length = length

for k in range(length_array.size):
    te_design.length = length_array[k]
    te_design.solve_te_pair()
    print "k =", k
    for i in range(current_array.size):
        te_design.I = current_array[i]
        te_design.solve_te_pair()
        power_height_I[k, i] = te_design.P_flux

te_design.I = current
te_design.fill_fraction = fill_fraction
te_design.length = length

data_dir = '../output/te_design_space/'
np.save(data_dir + 'power_I_fill', power_I_fill)
np.save(data_dir + 'power_fill_height', power_fill_height)
np.save(data_dir + 'power_height_I', power_height_I)
np.save(data_dir + 'current_array', current_array)
np.save(data_dir + 'fill_array', fill_array)
np.save(data_dir + 'length_array', length_array)

print "\nProgram finished."
print "\nPlotting..."

execfile('plot_TE_sensitivity.py')
