# Chad Baker
# Created on 2011 Nov 14

# Distribution Modules
import scipy as sp
import matplotlib.pyplot as plt
import os, sys

# User Defined Modules

cmd_folder = os.path.dirname(os.path.abspath('../Modules/hx.py'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import transient
reload(transient)

area = (0.002)**2
length = 1.e-3
current = 4.
area_ratio = 0.69
fill_fraction = 1. / 40.

hx_trans = transient.Transient_HX()
hx_trans.tem.method = 'analytical'
hx_trans.width = 30.e-2
hx_trans.exh.bypass = 0.
hx_trans.exh.height = 3.5e-2
hx_trans.cool.mdot = 1.
hx_trans.length = 1.
hx_trans.tem.I = current
hx_trans.tem.length = length

hx_trans.tem.Ptype.material = 'HMS'
hx_trans.tem.Ntype.material = 'MgSi'

hx_trans.tem.Ptype.area = area                           
hx_trans.tem.Ntype.area = hx_trans.tem.Ptype.area * area_ratio
hx_trans.tem.area_void = ( (1. - fill_fraction) / fill_fraction *
                           (hx_trans.tem.Ptype.area +
                            hx_trans.tem.Ntype.area) )  

hx_trans.type = 'parallel'

hx_trans.exh.T_inlet = 800.
hx_trans.exh.P = 100.
hx_trans.cool.T_inlet = 300.

hx_trans.set_mdot_charge()
hx_trans.solve_hx_transient()

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
plt.plot(hx_trans.x_dim * 100., hx_trans.exh.T_nodes, 'sr', label='Exhaust')
plt.plot(hx_trans.x_dim * 100., hx_trans.tem.T_h_nodes, 'sg', label='TEM Hot Side')
plt.plot(hx_trans.x_dim * 100., hx_trans.tem.T_c_nodes, 'sk', label='TEM Cold Side')
plt.plot(hx_trans.x_dim * 100., hx_trans.cool.T_nodes, 'sb', label='Coolant')

plt.xlabel('Distance Along HX (cm)')
plt.ylabel('Temperature (K)')
#plt.title('Temperature v. Distance, '+hx_trans.type)
plt.grid()
plt.legend(loc='best')
plt.subplots_adjust(bottom=0.15)
plt.savefig('Plots/' + hx_trans.tem.method + '/' + 'temp.png')
plt.savefig('Plots/' + hx_trans.tem.method + '/' + 'temp.pdf')

plt.figure()
plt.plot(hx_trans.x_dim * 100., hx_trans.tem.power_nodes * 1000., 's', label='Exhaust')

plt.xlabel('Distance Along HX (cm)')
plt.ylabel('TEG Power (W)')
plt.grid()
plt.legend(loc='best')
plt.subplots_adjust(bottom=0.15)
plt.savefig('Plots/' + hx_trans.tem.method + '/' + 'TEG power.png')
plt.savefig('Plots/' + hx_trans.tem.method + '/' + 'TEG power.pdf')

# plt.show()

print hx_trans.power_net

os.chdir('Instances')
