# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import matplotlib.pyplot as plt
import os, sys
from scipy.optimize import fsolve

# User Defined Modules

cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import hx
reload(hx)
    
leg_area = (0.002)**2

area_ratio = 0.659
fill_fraction = 2.13e-2
leg_length = 1.10e-3
current = 4.10

hx_inst = hx.HX()
hx_inst.te_pair.method = 'numerical'
hx_inst.width = 30.e-2
hx_inst.exh.height = 3.5e-2
hx_inst.cool.mdot = 1.
hx_inst.length = 1.
hx_inst.te_pair.I = current
hx_inst.te_pair.length = leg_length

hx_inst.te_pair.Ptype.material = 'HMS'
hx_inst.te_pair.Ntype.material = 'MgSi'

hx_inst.te_pair.Ptype.area = leg_area                           
hx_inst.te_pair.Ntype.area = hx_inst.te_pair.Ptype.area * area_ratio
hx_inst.te_pair.area_void = ( (1. - fill_fraction) / fill_fraction *
                           (hx_inst.te_pair.Ptype.area +
                            hx_inst.te_pair.Ntype.area) )  

hx_inst.type = 'counter'

hx_inst.exh.T_inlet = 800.
hx_inst.cool.T_inlet_set = 300.
hx_inst.cool.T_outlet = 310.

hx_inst.set_mdot_charge()
# hx_inst.cool.T_outlet = fsolve(hx_inst.get_T_inlet_error, x0=hx_inst.cool.T_outlet)
hx_inst.solve_hx()

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

plt.close('all')

plt.figure()
plt.plot(hx_inst.x_dim * 100., hx_inst.exh.T_nodes, 'sr', label='Exhaust')
plt.plot(hx_inst.x_dim * 100., hx_inst.te_pair.T_h_nodes, 'sg', label='TE_PAIR Hot Side')
plt.plot(hx_inst.x_dim * 100., hx_inst.te_pair.T_c_nodes, 'sk', label='TE_PAIR Cold Side')
plt.plot(hx_inst.x_dim * 100., hx_inst.cool.T_nodes, 'sb', label='Coolant')

plt.xlabel('Distance Along HX (cm)')
plt.ylabel('Temperature (K)')
#plt.title('Temperature v. Distance, '+hx_inst.type)
plt.grid()
plt.legend(loc='best')
plt.subplots_adjust(bottom=0.15)
plt.savefig('../Plots/' + hx_inst.te_pair.method + '/' + 'temp.png')
plt.savefig('../Plots/' + hx_inst.te_pair.method + '/' + 'temp.pdf')

plt.figure()
plt.plot(hx_inst.x_dim * 100., hx_inst.te_pair.power_nodes, 's', label='Exhaust')

plt.xlabel('Distance Along HX (cm)')
plt.ylabel('TEG Power (W)')
plt.grid()
plt.legend(loc='best')
plt.subplots_adjust(bottom=0.15)
plt.savefig('../Plots/' + hx_inst.te_pair.method + '/' + 'TEG power.png')
plt.savefig('../Plots/' + hx_inst.te_pair.method + '/' + 'TEG power.pdf')

plt.figure()
plt.plot(hx_inst.x_dim * 100., hx_inst.exh.availability_flow_nodes, label='exhaust')
plt.plot(hx_inst.x_dim * 100., hx_inst.cool.availability_flow_nodes, label='coolant')

plt.xlabel('Distance Along HX (cm)')
plt.ylabel('Availability (kW)')
plt.grid()
plt.legend(loc='best')
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.18)
plt.savefig('../Plots/' + hx_inst.te_pair.method + '/' + 'availability.png')
plt.savefig('../Plots/' + hx_inst.te_pair.method + '/' + 'availability.pdf')

# plt.show()

print "power net:", hx_inst.power_net * 1000., 'W'
print "power raw:", hx_inst.te_pair.power_total * 1000., 'W'
print "pumping power:", hx_inst.Wdot_pumping * 1000., 'W'
hx_inst.exh.volume = hx_inst.exh.height * hx_inst.exh.width * hx_inst.length
print "exhaust volume:", hx_inst.exh.volume * 1000., 'L'
print "exhaust power density:", hx_inst.power_net / hx_inst.exh.volume, 'kW/m^3'
