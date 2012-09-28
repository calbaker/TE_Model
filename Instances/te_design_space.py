# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import numpy as np
import os
import sys
import time

# User Defined Modules
cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import te_pair
reload(te_pair)

te_design = te_pair.TE_Pair()
# instantiate a te_design object

te_design.Ntype.material = 'MgSi'
te_design.Ptype.material = 'HMS'
# declare materials to be used for property calculations

fill_fraction = 4e-2
current = 24.
length = 4.00e-4
area_ratio = 0.7

te_design.fill_fraction = fill_fraction
te_design.I = current
te_design.length = length
te_design.leg_area_ratio = area_ratio

te_design.set_leg_areas()

te_design.T_c_conv = 300.  # cold side convection temperature (K)
te_design.T_h_conv = 680.  # hot side convection temperature (K)

te_design.U_cold = 8.
# cold side overall heat transfer coeffcient (kW / (m ** 2 * K))
te_design.U_hot = 2.
# hot side overall heat transfer coeffcient (kW / (m ** 2 * K))

te_design.optimize()

leg_area_ratio = te_design.leg_area_ratio
fill_fraction = te_design.fill_fraction
length = te_design.length
current = te_design.I

SIZE = 10
current_array = np.linspace(0.5, 2, SIZE) * te_design.I
fill_array = (
    np.linspace(0.5, 2, current_array.size + 1) *
    te_design.fill_fraction
    )
length_array = (
    np.linspace(0.5, 2, fill_array.size + 1) * te_design.length
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

t0 = time.clock()
for index in np.ndindex(current_array.size, fill_array.size):
    i = index[0]
    j = index[1]
    if j == 0:
        print "i =", i
    te_design.I = current_array[i]
    te_design.fill_fraction = fill_array[j]
    te_design.set_leg_areas()
    te_design.solve_te_pair()
    power_I_fill[i, j] = te_design.P_flux

te_design.I = current
te_design.fill_fraction = fill_fraction
te_design.length = length

t1 = time.clock() - t0
print "t1 =", t1
t0 = time.clock()
for index in np.ndindex(fill_array.size, length_array.size):
    j = index[0]
    k = index[1]
    te_design.fill_fraction = fill_array[j]
    te_design.set_leg_areas()
    if k == 0:
        print "j =", j
    te_design.length = length_array[k]
    te_design.solve_te_pair()
    power_fill_height[j, k] = te_design.P_flux

te_design.I = current
te_design.fill_fraction = fill_fraction
te_design.length = length
te_design.set_leg_areas()

t2 = time.clock() - t0
print "t2 =", t2
for index in np.ndindex(length_array.size, current_array.size):
    k = index[0]
    i = index[1]
    te_design.length = length_array[k]
    te_design.solve_te_pair()
    if i == 0:
        print "k =", k
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

execfile('plot_te_design_space.py')
