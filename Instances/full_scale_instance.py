# Chad Baker
# Created on 2011 Feb 10

# Distribution Modules
import scipy as sp
import matplotlib.pyplot as plt
import os, sys

# User Defined Modules

cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import hx
reload(hx)
    
area = (0.002)**2
length = 1.e-3
current = 4.
area_ratio = 0.69
fill_fraction = 1. / 40.

hx_inst = hx.HX()
hx_inst.tem.method = 'analytical'
hx_inst.width = 30.e-2
hx_inst.exh.bypass = 0.
hx_inst.exh.height = 3.5e-2
hx_inst.cool.mdot = 1.
hx_inst.length = 1.
hx_inst.tem.I = current
hx_inst.tem.length = length

hx_inst.tem.Ptype.material = 'HMS'
hx_inst.tem.Ntype.material = 'MgSi'

hx_inst.tem.Ptype.area = area                           
hx_inst.tem.Ntype.area = hx_inst.tem.Ptype.area * area_ratio
hx_inst.tem.area_void = ( (1. - fill_fraction) / fill_fraction *
                           (hx_inst.tem.Ptype.area +
                            hx_inst.tem.Ntype.area) )  

hx_inst.type = 'counter'

hx_inst.exh.T_inlet = 800.
hx_inst.exh.P = 100.
hx_inst.cool.T_outlet = 310.

hx_inst.set_mdot_charge()
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
plt.plot(hx_inst.x_dim * 100., hx_inst.tem.power_nodes * 1000., 's', label='Exhaust')

plt.xlabel('Distance Along HX (cm)')
plt.ylabel('TEG Power (W)')
plt.grid()
plt.legend(loc='best')
plt.subplots_adjust(bottom=0.15)
plt.savefig('../Plots/' + hx_inst.tem.method + '/' + 'TEG power.png')
plt.savefig('../Plots/' + hx_inst.tem.method + '/' + 'TEG power.pdf')

# plt.show()

print hx_inst.power_net

