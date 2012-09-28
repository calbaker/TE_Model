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
import te_pair
reload(te_pair)

te_minpar = te_pair.TE_Pair()
# instantiate a te_minpar object

te_minpar.Ntype.material = 'MgSi'
te_minpar.Ptype.material = 'HMS'
# declare materials to be used for property calculations

fill_fraction = 4.e-2
current = 24.
length = 4.00e-4
area_ratio = 0.7

te_minpar.fill_fraction = fill_fraction
te_minpar.I = current
te_minpar.length = length
te_minpar.leg_area_ratio = area_ratio

te_minpar.set_leg_areas()

te_minpar.T_c_conv = 300.  # cold side convection temperature (K)
te_minpar.T_h_conv = 800.

te_minpar.U_cold = 8.
# cold side overall heat transfer coeffcient (kW / (m ** 2 * K))
te_minpar.U_hot = 2.
# hot side overall heat transfer coeffcient (kW / (m ** 2 * K))

te_minpar.optimize()

SIZE = 10
current = np.zeros(SIZE)
fill_fraction = np.zeros(SIZE)
length = np.zeros(SIZE)
area_ratio = np.zeros(SIZE)
power = np.zeros(SIZE)

T_h_conv = np.linspace(550, 800., SIZE)

for i in range(SIZE):
    te_minpar.T_h_conv = T_h_conv[i]
    print "\nT_h_conv =", T_h_conv[i]

    te_minpar.optimize()

    current[i] = te_minpar.I
    fill_fraction[i] = te_minpar.fill_fraction
    length[i] = te_minpar.length
    area_ratio[i] = te_minpar.leg_area_ratio
    power[i] = te_minpar.P

data_dir = '../output/minpar_v_Th/'

np.save(data_dir + 'T_h_conv', T_h_conv)

np.save(data_dir + 'current', current)
np.save(data_dir + 'fill_fraction', fill_fraction)
np.save(data_dir + 'length', length)
np.save(data_dir + 'area_ratio', area_ratio)

np.save(data_dir + 'power', power)

print "\nProgram finished."
print "\nPlotting..."

execfile('plot_minpar_v_Th.py')
