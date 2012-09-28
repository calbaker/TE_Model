# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import numpy as np
import os
import sys

# User Defined Modules
cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import hx
reload(hx)

leg_area = (0.002)**2

area_ratio = 0.697
fill_fraction = 6.80e-2
leg_length = 0.503e-3
current = 20.5

hx_design = hx.HX()

hx_design.width = 0.55
hx_design.exh.height = 3.5e-2
hx_design.length = 0.55
hx_design.te_pair.I = current
hx_design.te_pair.length = leg_length
hx_design.te_pair.leg_area_ratio = area_ratio
hx_design.te_pair.fill_fraction = fill_fraction

hx_design.te_pair.set_leg_areas()

hx_design.te_pair.Ntype.material = 'MgSi'
hx_design.te_pair.Ptype.material = 'HMS'

hx_design.type = 'counter'

hx_design.exh.enh = hx_design.exh.set_enhancement('IdealFin')
hx_design.exh.enh.thickness = 1.e-3
hx_design.exh.enh.spacing = 1.26e-3

hx_design.cool.enh = hx_design.cool.set_enhancement('IdealFin')
hx_design.cool.enh.thickness = 1.e-3
hx_design.cool.enh.spacing = 1.e-3

hx_design.exh.T_inlet = 800.
hx_design.cool.T_inlet_set = 300.
hx_design.cool.T_outlet = 310.

hx_design.set_mdot_charge()
hx_design.solve_hx()
hx_design.optimize()

leg_area_ratio = hx_design.te_pair.leg_area_ratio
fill_fraction = hx_design.te_pair.fill_fraction
length = hx_design.te_pair.length
current = hx_design.te_pair.I

SIZE = 50
current_array = np.linspace(0.5, 2, SIZE) * hx_design.te_pair.I
fill_array = (
    np.linspace(0.5, 2, current_array.size + 1) *
    hx_design.te_pair.fill_fraction
    )
length_array = (
    np.linspace(0.5, 2, fill_array.size + 1) * hx_design.te_pair.length
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
    hx_design.te_pair.I = current_array[i]
    print "i =", i
    for j in range(fill_array.size):
        hx_design.te_pair.fill_fraction = fill_array[j]
        hx_design.te_pair.set_leg_areas()
        hx_design.solve_hx()
        power_I_fill[i, j] = hx_design.power_net

hx_design.te_pair.I = current
hx_design.te_pair.fill_fraction = fill_fraction
hx_design.te_pair.length = length

for j in range(fill_array.size):
    hx_design.te_pair.fill_fraction = fill_array[j]
    hx_design.te_pair.set_leg_areas()
    print "j =", j
    for k in range(length_array.size):
        hx_design.te_pair.length = length_array[k]
        hx_design.solve_hx()
        power_fill_height[j, k] = hx_design.power_net

hx_design.te_pair.I = current
hx_design.te_pair.fill_fraction = fill_fraction
hx_design.te_pair.length = length
hx_design.te_pair.set_leg_areas()

for k in range(length_array.size):
    hx_design.te_pair.length = length_array[k]
    hx_design.solve_hx()
    print "k =", k
    for i in range(current_array.size):
        hx_design.te_pair.I = current_array[i]
        hx_design.solve_hx()
        power_height_I[k, i] = hx_design.power_net

hx_design.te_pair.I = current
hx_design.te_pair.fill_fraction = fill_fraction
hx_design.te_pair.length = length

data_dir = '../output/hx_design_space/'
np.save(data_dir + 'power_I_fill', power_I_fill)
np.save(data_dir + 'power_fill_height', power_fill_height)
np.save(data_dir + 'power_height_I', power_height_I)
np.save(data_dir + 'current_array', current_array)
np.save(data_dir + 'fill_array', fill_array)
np.save(data_dir + 'length_array', length_array)

print "\nProgram finished."
print "\nPlotting..."

execfile('plot_hx_design_space.py')
