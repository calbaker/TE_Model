"""This script runs the model for designs available from heat sink
usa.  This doc string may not be completely accurate."""

# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import matplotlib.pyplot as plt
import os
import sys
import time

# User Defined Modules
cmd_folder = os.path.dirname('../Modules/')
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import hx
reload(hx)

time0 = time.clock()

leg_area = (0.002) ** 2

area_ratio = 0.849
fill_fraction = 3.85e-2
leg_length = 4.00e-4
current = 13.2

time0 = time.clock()

hx_exp = hx.HX()

hx_exp.width = (20. - 0.640) * 2.54e-2
hx_exp.exh.height = (2.5 - 0.375) * 2.54e-2
hx_exp.cool.height = 1.25 * 2.54e-2
hx_exp.length = 20. * 2.54e-2

hx_exp.plate.thickness = 0.375 * 2.54e-2

hx_exp.te_pair.leg_area_ratio = area_ratio
hx_exp.te_pair.fill_fraction = fill_fraction
hx_exp.te_pair.I = current
hx_exp.te_pair.length = leg_length

hx_exp.te_pair.set_leg_areas()

hx_exp.te_pair.Ntype.material = 'MgSi'
hx_exp.te_pair.Ptype.material = 'HMS'

hx_exp.te_pair.method = 'numerical'
hx_exp.type = 'counter'

thickness = 0.080 * 2.54e-2
spacing = (0.400 - 0.080) * 2.54e-2

hx_exp.exh.enh = hx_exp.exh.enh_lib.IdealFin()
hx_exp.exh.enh.thickness = thickness
hx_exp.exh.enh.spacing = (0.200 - 0.080) * 2.54e-2
hx_exp.exh.enh.l = 3. / 8. * 2.54e-2

hx_exp.cool.enh = hx_exp.cool.enh_lib.IdealFin()
hx_exp.cool.enh.thickness = thickness
hx_exp.cool.enh.spacing = (0.400 - 0.080) * 2.54e-2

# hx_exp.apar_list.append(['self','exh','enh','l'])
# hx_exp.apar_list.append(['self','length'])

hx_exp.exh.T_inlet = 800.
hx_exp.cool.T_inlet_set = 300.
hx_exp.cool.T_outlet = 307.7

hx_exp.set_mdot_charge()

hx_exp.solve_hx()

# def get_minpar(length):
#     """Returns inverse of net power for varied length."""
#     hx_exp.length = length
#     hx_exp.solve_hx()

#     if hx_exp.power_net > 0:
#         minpar = 1. / hx_exp.power_net
#     else:
#         minpar = np.abs(hx_exp.power_net)

#     return minpar

# length = fmin(get_minpar, x0=1.)

print "power net:", hx_exp.power_net * 1000., 'W'
print "power raw:", hx_exp.te_pair.power_total * 1000., 'W'
print "pumping power:", hx_exp.Wdot_pumping * 1000., 'W'
hx_exp.exh.volume = hx_exp.exh.height * hx_exp.exh.width * hx_exp.length
print "exhaust volume:", hx_exp.exh.volume * 1000., 'L'
print "exhaust power density:", hx_exp.power_net / hx_exp.exh.volume, 'kW/m^3'

elapsed = time.clock() - time0
print "\nelapsed time:", elapsed, "s"

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
plt.plot(hx_exp.x * 100., hx_exp.exh.T_nodes, '-r', label='Exhaust')
plt.plot(hx_exp.x * 100., hx_exp.te_pair.T_h_nodes, '-g',
         label='TE_PAIR Hot Side')
plt.plot(hx_exp.x * 100., hx_exp.te_pair.T_c_nodes, '-k',
         label='TE_PAIR Cold Side')
plt.plot(hx_exp.x * 100., hx_exp.cool.T_nodes, '-b', label='Coolant')

plt.xlabel('Distance Along HX (cm)')
plt.ylabel('Temperature (K)')
#plt.title('Temperature v. Distance, '+hx_exp.type)
plt.grid()
# plt.legend(loc='center left')
plt.subplots_adjust(bottom=0.15)
# plt.savefig('../Plots/temp '+hx_exp.type+str(hx_exp.exh.fins)+'.png')
# plt.savefig('../Plots/temp '+hx_exp.type+str(hx_exp.exh.fins)+'.pdf')

# plt.show()
