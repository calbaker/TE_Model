# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import scipy as sp
import matplotlib.pyplot as plt
import os, sys
from scipy.optimize import fsolve

# User Defined Modules

cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import hx
reload(hx)
    
# parameters from xmin2
# 7.049488398024472691e-01
# 2.074354421989454272e-02
# 1.033370547666811676e-03
# 4.634972529966798760e+00

leg_area = (0.002)**2
leg_length = 1.03e-3
current = 4.63
area_ratio = 0.705
fill_fraction = 2.07e-2

hx_inst = hx.HX()
hx_inst.tem.method = 'analytical'
hx_inst.width = 30.e-2
hx_inst.exh.height = 3.5e-2
hx_inst.cool.mdot = 1.
hx_inst.length = 1.
hx_inst.tem.I = current
hx_inst.tem.length = leg_length

hx_inst.tem.Ptype.material = 'HMS'
hx_inst.tem.Ntype.material = 'MgSi'

hx_inst.tem.Ptype.area = leg_area                           
hx_inst.tem.Ntype.area = hx_inst.tem.Ptype.area * area_ratio
hx_inst.tem.area_void = ( (1. - fill_fraction) / fill_fraction *
                           (hx_inst.tem.Ptype.area +
                            hx_inst.tem.Ntype.area) )  

hx_inst.type = 'counter'

hx_inst.exh.T_inlet = 800.
hx_inst.cool.T_inlet_set = 300.
hx_inst.cool.T_outlet = 310.

hx_inst.set_mdot_charge()
hx_inst.cool.T_outlet = fsolve(hx_inst.get_T_inlet_error, x0=hx_inst.cool.T_outlet)
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
plt.plot(hx_inst.x_dim * 100., hx_inst.tem.T_h_nodes, 'sg', label='TEM Hot Side')
plt.plot(hx_inst.x_dim * 100., hx_inst.tem.T_c_nodes, 'sk', label='TEM Cold Side')
plt.plot(hx_inst.x_dim * 100., hx_inst.cool.T_nodes, 'sb', label='Coolant')

plt.xlabel('Distance Along HX (cm)')
plt.ylabel('Temperature (K)')
#plt.title('Temperature v. Distance, '+hx_inst.type)
plt.grid()
plt.legend(loc='best')
plt.subplots_adjust(bottom=0.15)
plt.savefig('../Plots/' + hx_inst.tem.method + '/' + 'temp.png')
plt.savefig('../Plots/' + hx_inst.tem.method + '/' + 'temp.pdf')

plt.figure()
plt.plot(hx_inst.x_dim * 100., hx_inst.tem.power_nodes, 's', label='Exhaust')

plt.xlabel('Distance Along HX (cm)')
plt.ylabel('TEG Power (W)')
plt.grid()
plt.legend(loc='best')
plt.subplots_adjust(bottom=0.15)
plt.savefig('../Plots/' + hx_inst.tem.method + '/' + 'TEG power.png')
plt.savefig('../Plots/' + hx_inst.tem.method + '/' + 'TEG power.pdf')

plt.figure()
plt.plot(hx_inst.x_dim * 100., hx_inst.exh.availability_flow_nodes, label='exhaust')
plt.plot(hx_inst.x_dim * 100., hx_inst.cool.availability_flow_nodes, label='coolant')

plt.xlabel('Distance Along HX (cm)')
plt.ylabel('Availability (kW)')
plt.grid()
plt.legend(loc='best')
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.18)
plt.savefig('../Plots/' + hx_inst.tem.method + '/' + 'availability.png')
plt.savefig('../Plots/' + hx_inst.tem.method + '/' + 'availability.pdf')

# plt.show()

print hx_inst.power_net

