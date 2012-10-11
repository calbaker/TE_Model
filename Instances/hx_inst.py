# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import matplotlib.pyplot as plt
import os,sys
from scipy.optimize import fsolve

# User Defined Modules
cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import hx
reload(hx)

leg_area = (0.002)**2

area_ratio = 0.745
fill_fraction = 3.10e-2
leg_length = 3.56e-4
current = 13.0

hx_empty = hx.HX()

hx_empty.width = 20. * 2.54e-2
hx_empty.exh.height = 2.5 * 2.54e-2
hx_empty.cool.height = 1. * 2.54e-2
hx_empty.length = 20. * 2.54e-2

hx_empty.te_pair.I = current
hx_empty.te_pair.length = leg_length
hx_empty.te_pair.leg_area_ratio = area_ratio
hx_empty.te_pair.fill_fraction = fill_fraction

hx_empty.te_pair.set_leg_areas()

hx_empty.te_pair.Ntype.material = 'MgSi'
hx_empty.te_pair.Ptype.material = 'HMS'

hx_empty.type = 'counter'

hx_empty.exh.T_inlet = 800.
hx_empty.cool.T_inlet_set = 300.
hx_empty.cool.T_outlet = 310.

hx_empty.set_mdot_charge()
# hx_empty.cool.T_outlet = fsolve(hx_empty.get_T_inlet_error,
#                                 x0=hx_empty.cool.T_outlet, xtol=0.01)
hx_empty.solve_hx()

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

plt.figure()
plt.plot(hx_empty.x * 100., hx_empty.exh.T_nodes, '-r', label='Exhaust')
plt.plot(hx_empty.x * 100., hx_empty.te_pair.T_h_nodes, '-g', label='TE Hot Side')
plt.plot(hx_empty.x * 100., hx_empty.te_pair.T_c_nodes, '-k', label='TE Cold Side')
plt.plot(hx_empty.x * 100., hx_empty.cool.T_nodes, '-b', label='Coolant')

plt.xlabel('Distance Along HX (cm)')
plt.ylabel('Temperature (K)')
#plt.title('Temperature v. Distance, '+hx_empty.type)
plt.grid()
# plt.legend(loc='center left')
plt.subplots_adjust(bottom=0.15)
plt.ylim(ymax=950)
plt.legend(loc="upper right")
plt.savefig('../Plots/fin_inst/temp.png')
plt.savefig('../Plots/fin_inst/temp.pdf')

# plt.show()

print "power net:", hx_empty.power_net * 1000., 'W'
print "power raw:", hx_empty.te_pair.power_total * 1000., 'W'
print "pumping power:", hx_empty.Wdot_pumping * 1000., 'W'
hx_empty.exh.volume = hx_empty.exh.height * hx_empty.exh.width * hx_empty.length
print "exhaust volume:", hx_empty.exh.volume * 1000., 'L'
print "exhaust power density:", hx_empty.power_net / hx_empty.exh.volume, 'kW/m^3'


